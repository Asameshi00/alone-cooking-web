# cooking-web-backend

FastAPI で構築した cooking-web 向けバックエンドです。

## 機能
- レシピ検索 (楽天レシピ API)
- AI レシピ提案 (OpenAI / Gemini。未設定時はローカル生成)
- 在庫管理 API
- お気に入りレシピ API
- OpenAPI 自動生成 (`/docs`, `/openapi.json`)

## セットアップ
1. Python 3.11+ を用意
2. 依存関係をインストール
   - `uv sync`
3. 環境変数を作成
   - `.env.example` を `.env` にコピーして編集
4. 起動
   - `uv run uvicorn app.main:app --reload --port 8000`

## 主なエンドポイント
- `GET /api/v1/health`
- `GET /api/v1/recipes/search?ingredient=卵&limit=10`
- `POST /api/v1/ai/suggest`
- `GET /api/v1/inventory`
- `POST /api/v1/inventory`
- `GET /api/v1/favorites`
- `POST /api/v1/favorites`
