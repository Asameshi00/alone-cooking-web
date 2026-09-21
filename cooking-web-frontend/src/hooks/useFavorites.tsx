import { useCallback, useState } from "react";
import { Favorite, FavoriteItem, FavoriteKind, FavoriteRaw } from "../types/favorite";

// お気に入りの状態管理を行うカスタムフックの型定義
interface UseFavoritesReturn {
    favorites: Favorite[];
    loading: boolean;
    error: string | null;
    fetchFavorites: (userId: number) => Promise<Favorite[]>;
    addFavorite: (item: FavoriteItem, userId: number) => Promise<Favorite | null>;
    removeFavorite: (itemId: string, kind: FavoriteKind, userId: number) => Promise<boolean>;
}

// バックエンドAPIのURL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ?? "http://localhost:8000/api/v1";

// バックエンドAPIのレスポンスをFavorite型に変換する
const mapRawToFavorite = (raw: FavoriteRaw): Favorite => ({
    id: raw.id,
    userId: raw.user_id,
    kind: raw.kind,
    itemId: raw.item_id,
    title: raw.title,
    description: raw.description,
    url: raw.url,
    imageUrl: raw.image_url,
    createdAt: raw.created_at,
});

// お気に入りの状態管理を行うカスタムフック
export const useFavorites = (): UseFavoritesReturn => {
    const [favorites, setFavorites] = useState<Favorite[]>([]);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);

    // お気に入りを取得する
    // APIのURLにGETリクエストを送信してお気に入りを取得する
    const fetchFavorites = useCallback(async (userId: number) => {
        setLoading(true);
        setError(null);
        try {
            const response = await fetch(`${API_BASE_URL}/recipes/favorites?user_id=${userId}`);
            if (!response.ok) {
                throw new Error(`お気に入りの取得に失敗しました: ${response.status}`);
            }
            const jsonData: FavoriteRaw[] = await response.json();
            const mapped: Favorite[] = jsonData.map(mapRawToFavorite);
            setFavorites(mapped);
            return mapped;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : "不明なエラーが発生しました";
            setError(errorMessage);
            setFavorites([]);
            return [];
        } finally {
            setLoading(false);
        }
    }, []);

    // お気に入りを追加する
    // APIのURLにPOSTリクエストを送信してお気に入りを追加する
    const addFavorite = useCallback(async (item: FavoriteItem, userId: number) => {
        setError(null);
        try {
            // APIのURLにPOSTリクエストを送信してお気に入りを追加する
            const response = await fetch(`${API_BASE_URL}/recipes/favorites`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ user_id: userId, ...item }),
            });
            // リクエストが失敗した場合エラーを投げる
            if (!response.ok) {
                throw new Error(`お気に入りの登録に失敗しました: ${response.status}`);
            }
            const data: FavoriteRaw = await response.json();
            const favorite = mapRawToFavorite(data);
            setFavorites((prev) => (prev.some((f) => f.itemId === favorite.itemId && f.kind === favorite.kind)
                ? prev
                : [...prev, favorite]));
            // お気に入りを状態に保存する
            return favorite;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : "不明なエラーが発生しました";
            setError(errorMessage);
            return null;
        } finally {
            setLoading(false);
        }
    }, []);

    // お気に入りを解除する
    // APIのURLにDELETEリクエストを送信してお気に入りを解除する
    const removeFavorite = useCallback(async (itemId: string, kind: FavoriteKind, userId: number) => {
        setError(null);
        try {
        const response = await fetch(
            `${API_BASE_URL}/recipes/favorites?user_id=${userId}&item_id=${encodeURIComponent(itemId)}&kind=${kind}`,
            { method: "DELETE" }
        );
        if (!response.ok && response.status !== 404) {
            throw new Error(`お気に入りの解除に失敗しました: ${response.status}`);
        }
            // 204はボディ無しのためresponse.json()を呼ばない。404（既に削除済み）も成功扱いにする。
            setFavorites((prev) => prev.filter((f) => !(f.itemId === itemId && f.kind === kind)));
            return true;
        } catch (err) {
            const errorMessage = err instanceof Error ? err.message : "不明なエラーが発生しました";
            setError(errorMessage);
            return false;
        }
    }, []);

    return { favorites, loading, error, fetchFavorites, addFavorite, removeFavorite };
}

export default useFavorites;
