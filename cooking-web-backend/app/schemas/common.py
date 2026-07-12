# !/usr/bin/env python
# -*- coding: utf-8 -*-


from pydantic import BaseModel, ConfigDict

# APIのメッセージ
class APIMessage(BaseModel):
    message: str

# ORMの基底モデル
class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
