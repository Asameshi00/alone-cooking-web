/** お気に入りの種類（レシピ or 動画） **/
export type FavoriteKind = "recipe" | "video";

/** お気に入り登録済みアイテム **/
export type Favorite = {
    id: number;
    userId: number;
    kind: FavoriteKind;
    itemId: string;
    title: string;
    description: string | null;
    url: string;
    imageUrl: string | null;
    createdAt: string;
};

/** バックエンドAPIレスポンスの生データ **/
export type FavoriteRaw = {
    id: number;
    user_id: number;
    kind: FavoriteKind;
    item_id: string;
    title: string;
    description: string | null;
    url: string;
    image_url: string | null;
    created_at: string;
};

/** お気に入り登録リクエストに必要な最小限の情報（レシピ/動画カードから作る） **/
export type FavoritableItem = {
    kind: FavoriteKind;
    item_id: string;
    title: string;
    description: string;
    url: string;
    image_url: string | null;
};
