# !/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field

# AIによるレシピ提案を行うリクエスト
class AISuggestionRequest(BaseModel):
    leftovers: list[str] = Field(default_factory=list) # 余り物
    bargain_items: list[str] = Field(default_factory=list) # 特売品

# AIによるレシピ提案を行うレスポンス
class AISuggestionResponse(BaseModel):
    provider: str # AI
    recipe_title: str # レシピのタイトル
    recipe_description: str # レシピの説明
    steps: list[str] # レシピの手順
    tips: list[str] # レシピのヒント
    time: int # レシピのおおよその所要時間(分)
