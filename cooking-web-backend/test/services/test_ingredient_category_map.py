# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import os

import httpx
import pytest

from app.services.ingredient_category_map import (
  INGREDIENT_ALIASES,
  INGREDIENT_CATEGORY_KEYWORDS,
  find_category_keywords,
)


def test_対応表は100種類の食材を持つ():
  assert len(INGREDIENT_CATEGORY_KEYWORDS) == 100
  assert all(INGREDIENT_CATEGORY_KEYWORDS.values())


def test_別名はすべて対応表のキーを指す():
  assert set(INGREDIENT_ALIASES.values()) <= set(INGREDIENT_CATEGORY_KEYWORDS)


@pytest.mark.parametrize(
  ("ingredient", "expected_key"),
  [
    ("玉ねぎ", "玉ねぎ"),
    ("たまねぎ", "玉ねぎ"),
    ("新たまねぎ", "玉ねぎ"),
    ("長ねぎ", "長ねぎ"),
    ("国産豚バラ肉", "豚バラ"),
    ("鶏むね肉", "鶏むね肉"),
    ("プチトマト", "ミニトマト"),
    ("人参 ", "にんじん"),
  ],
)
def test_表記ゆれや修飾語つきでも対応表のキーに寄せられる(ingredient, expected_key):
  assert find_category_keywords(ingredient) == INGREDIENT_CATEGORY_KEYWORDS[expected_key]


def test_対応表にない食材は空リスト():
  assert find_category_keywords("ドラゴンフルーツ") == []


@pytest.mark.skipif(
  os.getenv("RAKUTEN_LIVE_TEST") != "1",
  reason="楽天APIを実際に叩くため RAKUTEN_LIVE_TEST=1 のときだけ実行する",
)
def test_対応表の全食材が楽天のカテゴリにヒットする():
  from app.services.rakuten_service import RakutenRecipeService

  service = RakutenRecipeService()

  async def map_all() -> dict[str, str | None]:
    async with httpx.AsyncClient(timeout=20.0) as client:
      return {
        ingredient: await service.map_category_id_from_ingredient(ingredient, client)
        for ingredient in INGREDIENT_CATEGORY_KEYWORDS
      }

  results = asyncio.run(map_all())
  missed = [ingredient for ingredient, category_id in results.items() if category_id is None]
  assert missed == []
