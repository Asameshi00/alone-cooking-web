import json

import httpx

from app.core.config import get_settings
from app.schemas.ai import AISuggestionRequest, AISuggestionResponse


class AIRecipeService:
    def __init__(self) -> None:
        self.settings = get_settings()

    async def suggest(self, req: AISuggestionRequest) -> AISuggestionResponse:
        provider = self.settings.ai_provider.lower()
        if provider == "openai" and self.settings.openai_api_key:
            return await self._suggest_openai(req)
        if provider == "gemini" and self.settings.gemini_api_key:
            return await self._suggest_gemini(req)
        return self._suggest_local(req)

    async def _suggest_openai(self, req: AISuggestionRequest) -> AISuggestionResponse:
        prompt = self._build_prompt(req)
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        body = {
            "model": self.settings.openai_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            res = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
            res.raise_for_status()
            text = res.json()["choices"][0]["message"]["content"]
        return self._from_text("openai", text)

    async def _suggest_gemini(self, req: AISuggestionRequest) -> AISuggestionResponse:
        prompt = self._build_prompt(req)
        params = {"key": self.settings.gemini_api_key}
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.settings.gemini_model}:generateContent"
        async with httpx.AsyncClient(timeout=20.0) as client:
            res = await client.post(url, params=params, json=body)
            res.raise_for_status()
            text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
        return self._from_text("gemini", text)

    def _suggest_local(self, req: AISuggestionRequest) -> AISuggestionResponse:
        ingredients = req.leftovers + req.bargain_items
        base = ingredients[0] if ingredients else "旬の野菜"
        return AISuggestionResponse(
            provider="local",
            recipe_title=f"{base}のワンパン炒め",
            recipe_description="余り物と特売食材を無駄なく使う、シンプルで作りやすいレシピです。",
            steps=[
                "食材を食べやすい大きさに切る。",
                "フライパンに油を引き、火の通りにくい順に炒める。",
                "塩こしょうと醤油少々で味を整える。",
            ],
            tips=["冷蔵庫の残り野菜を優先して使う。", "最後にごま油を少し加えると香りが良くなる。"],
        )

    def _build_prompt(self, req: AISuggestionRequest) -> str:
        data = {
            "leftovers": req.leftovers,
            "bargain_items": req.bargain_items,
            "output_format": {
                "recipe_title": "string",
                "recipe_description": "string",
                "steps": ["string"],
                "tips": ["string"],
            },
        }
        return (
            "あなたは料理アシスタントです。次の食材から1つレシピを提案してください。"
            "回答はJSONのみで返してください。\n"
            f"{json.dumps(data, ensure_ascii=False)}"
        )

    def _from_text(self, provider: str, text: str) -> AISuggestionResponse:
        try:
            parsed = json.loads(text)
            return AISuggestionResponse(provider=provider, **parsed)
        except (json.JSONDecodeError, TypeError, KeyError):
            return AISuggestionResponse(
                provider=provider,
                recipe_title="AI提案レシピ",
                recipe_description=text[:280],
                steps=["AIの提案文を確認してください。"],
                tips=["入力食材を増やすと提案精度が上がります。"],
            )
