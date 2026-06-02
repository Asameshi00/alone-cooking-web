# cooking-web-backend

FastAPI で構築した cooking-web 向けバックエンド

---

## 目次
- [機能](#機能)
- [ディレクトリ構造とその役割](#ディレクトリ構造とその役割)
- [環境構築](#環境構築)
- [主なエンドポイント](#主なエンドポイント)

---

## 機能
- レシピ検索 (楽天レシピ API)
- AI レシピ提案 (OpenAI / Gemini 未設定時はローカル生成)
- 在庫管理 API
- お気に入りレシピ API
- OpenAPI 自動生成 (`/docs`, `/openapi.json`)


## ディレクトリ構造とその役割
```
cooking-web-backend
├── app # app
│   ├── api      # HTTPエンドポイント層でAPIの定義（controller層に当たる）
│   ├── core     # 共通設定・基盤（.envの読み込みを管理）
│   ├── db       # DB接続と初期化
│   ├── models   # DBテーブルの定義（model層に当たる）
│   ├── schemas  # リクエスト・レスポンスの型の定義
│   └── services # 外部APIや業務ロジックの定義
└── test
    ├── api      # app/apiのテストケース
    ├── core     # app/coreのテストケース
    ├── db       # app/dbのテストケース
    ├── schemas  # app/schemasのテストケース
    └── services # app/servicesのテストケース
```


## 環境構築
1. Python 3.11+ を用意
2. 依存関係をインストール
   - `uv sync`
3. 環境変数を作成
   - `.env.example` を `.env` にコピーして編集
4. 起動
   - `uv run uvicorn app.main:app --reload --port 8000`


## 主なエンドポイント
- `GET /api/v1/health`
   - GET method: ヘルスチェック
- `GET /api/v1/recipes/search?ingredient=卵&limit=10`
   - GET method: 食材をもとにレシピ検索
- `GET /api/v1/recipes/favorites`
   - GET method: お気に入りレシピを取得する
- `POST /api/v1/recipes/favorites`
   - POST method: お気に入りのレシピを作成する
- `GET /api/v1/inventory`
   - GET method: 在庫を取得する
- `POST /api/v1/inventory`
   - POST method: 在庫を作成する
- `DELETE /api/v1/inventory`
   - DELETE method: 在庫を削除する
