/**
 * お気に入り登録したレシピ・動画の一覧を表示する画面
 */

import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useFavorites } from "../../hooks/useFavorites";
import { DEMO_USER_ID } from "../../constants/user";
import { Favorite } from "../../types/favorite";
import FavoriteButton from "../../components/FavoriteButton";

const Favorites: React.FC = () => {
    const { loading, error, fetchFavorites } = useFavorites();
    const [items, setItems] = useState<Favorite[]>([]);

    // お気に入りを取得
    useEffect(() => {
        fetchFavorites(DEMO_USER_ID).then(setItems);
    }, [fetchFavorites]);

    // 一覧からその場で取り除く（APIへの削除リクエストはFavoriteButton側で完結している）
    const removeLocally = (itemId: string, kind: Favorite["kind"]) => {
        setItems((prev) => prev.filter((f) => !(f.itemId === itemId && f.kind === kind)));
    };

    const recipes = items.filter((f) => f.kind === "recipe");
    const videos = items.filter((f) => f.kind === "video");

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="bg-white shadow-md rounded-lg p-6">
                <h1 className="text-2xl font-bold text-center mb-4">お気に入り</h1>
                <Link to="/" className="mb-4 inline-block text-blue-600 underline">まな板に戻る</Link>

                {loading && <p className="text-sm text-gray-600">読み込み中...</p>}
                {error && <p className="text-sm text-red-600">{error}</p>}
                {!loading && items.length === 0 && (
                    <p className="text-sm text-gray-600">お気に入りはまだありません。</p>
                )}

                {recipes.length > 0 && (
                    <section className="mb-6">
                        <h3 className="text-sm font-semibold text-gray-600 mb-2">レシピ</h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {recipes.map((favorite) => (
                                <div key={favorite.itemId} className="rounded-md border bg-gray-50 p-3">
                                    <div className="flex items-start justify-between gap-2">
                                        <h4 className="font-semibold">{favorite.title}</h4>
                                        <FavoriteButton
                                            item={{
                                                kind: "recipe",
                                                item_id: favorite.itemId,
                                                title: favorite.title,
                                                description: favorite.description ?? "",
                                                url: favorite.url,
                                                image_url: favorite.imageUrl,
                                            }}
                                            userId={DEMO_USER_ID}
                                            isFavorite={true}
                                            onChange={() => removeLocally(favorite.itemId, favorite.kind)}
                                        />
                                    </div>
                                    {favorite.description && (
                                        <p className="text-sm text-gray-600">{favorite.description}</p>
                                    )}
                                    {favorite.imageUrl && (
                                        <img
                                            src={favorite.imageUrl}
                                            alt={favorite.title}
                                            className="mt-2 h-36 w-full object-cover rounded"
                                        />
                                    )}
                                    <a
                                        href={favorite.url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="mt-2 inline-block text-blue-600 underline"
                                    >
                                        レシピを見る
                                    </a>
                                </div>
                            ))}
                        </div>
                    </section>
                )}

                {videos.length > 0 && (
                    <section>
                        <h3 className="text-sm font-semibold text-gray-600 mb-2">動画</h3>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {videos.map((favorite) => (
                                <div key={favorite.itemId} className="rounded-md border bg-gray-50 p-3">
                                    <div className="flex items-start justify-between gap-2">
                                        <h4 className="font-semibold">{favorite.title}</h4>
                                        <FavoriteButton
                                            item={{
                                                kind: "video",
                                                item_id: favorite.itemId,
                                                title: favorite.title,
                                                description: favorite.description ?? "",
                                                url: favorite.url,
                                                image_url: favorite.imageUrl,
                                            }}
                                            userId={DEMO_USER_ID}
                                            isFavorite={true}
                                            onChange={() => removeLocally(favorite.itemId, favorite.kind)}
                                        />
                                    </div>
                                    {favorite.description && (
                                        <p className="text-sm text-gray-600 line-clamp-2">{favorite.description}</p>
                                    )}
                                    {favorite.imageUrl && (
                                        <img
                                            src={favorite.imageUrl}
                                            alt={favorite.title}
                                            className="mt-2 h-36 w-full object-cover rounded"
                                        />
                                    )}
                                    <a
                                        href={favorite.url}
                                        target="_blank"
                                        rel="noreferrer"
                                        className="mt-2 inline-block text-blue-600 underline"
                                    >
                                        動画を見る
                                    </a>
                                </div>
                            ))}
                        </div>
                    </section>
                )}
            </div>
        </div>
    );
};

export default Favorites;
