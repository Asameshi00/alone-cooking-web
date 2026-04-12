# イメージ指定
FROM python:3.12-slim-bookworm
# ワークディレクトリ指定
WORKDIR /app
# uvをインストール
RUN pip install --no-cache-dir uv
# pyproject.tomlとuv.lockをコピー
COPY pyproject.toml uv.lock ./
# uv sync --frozen --no-dev
RUN uv sync --frozen --no-dev
# appディレクトリをコピー
COPY app ./app
# ポートを指定
EXPOSE 8000
# uvicornを起動
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
