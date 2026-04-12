# イメージ指定
FROM node:20-bookworm-slim
# ワークディレクトリ指定
WORKDIR /app
# package.jsonとpackage-lock.jsonをコピー
COPY package.json package-lock.json ./
# npm ci
RUN npm ci
# .をコピー
COPY . .
# ポートを指定
EXPOSE 3000
# HOSTを指定
ENV HOST=0.0.0.0
# npm startを起動
CMD ["npm", "start"]
