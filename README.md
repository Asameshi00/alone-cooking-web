# cooking-web

### コンセプト
余り物の食材に困ったことはありませんか？
その食材を使ったレシピを提案してくれるwebサイトです！
ただレシピを探してくれるだけでなく、AIの提案機能も備わってます！

### ターゲット層
一人暮らしで自炊を心がけている人

### 機能
1. レシピ検索
  - 食材名から各種レシピを検索する。
2. 「手間の少なさ」「調理器具」での絞り込み
  - 「包丁を使わない」「フライパン1つ」「ワンボウル」「レンジのみ」「洗い物3点以下」など、調理プロセスや後片付けの負荷に基づく検索
3. 「爆速5分レシピ」「ほったらかし（放置時間）レシピ」など、作業時間と放置時間を分けた検索
4. 一人暮らし・節約派に向けたコンテキスト


### 開発環境
- 言語: TypeScript（React）・FastAPI
- デプロイ: vercel
- タスク・スケジュール管理: Notion

### 使用ツール
- バージョン管理: Git
- ソースコード管理: GitHub
- デザイン関連: Figma

### 使用API
- [楽天レシピAPI](https://webservice.rakuten.co.jp/documentation/recipe-category-list)
- [Youtube Data API](https://developers.google.com/youtube/v3/docs?hl=ja)
