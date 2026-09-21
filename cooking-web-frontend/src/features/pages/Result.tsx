/**
 * まな板の食材で検索したレシピ・動画の一覧を表示する画面
 */

import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { IngredientSearchResult } from '../../types/recipe';
import { useFavorites } from '../../hooks/useFavorites';
import { DEMO_USER_ID } from '../../constants/user';
import FavoriteButton from '../../components/FavoriteButton';

interface ResultLocationState {
    results?: IngredientSearchResult[];
}

const Result: React.FC = () => {
    const location = useLocation();
    const results = (location.state as ResultLocationState | null)?.results ?? [];

    const { favorites, fetchFavorites } = useFavorites();
    const [favoriteKeys, setFavoriteKeys] = useState<Set<string>>(new Set());

    // お気に入りを取得
    useEffect(() => {
        fetchFavorites(DEMO_USER_ID);
    }, [fetchFavorites]);

    // お気に入りのキーを更新
    useEffect(() => {
        setFavoriteKeys(new Set(favorites.map((f) => `${f.kind}:${f.itemId}`)));
    }, [favorites]);

    // 一覧のキー集合をその場で更新する（APIへの登録/解除はFavoriteButton側で完結している）
    const toggleKey = (key: string, nowFavorite: boolean) => {
        setFavoriteKeys((prev) => {
            const next = new Set(prev);
            if (nowFavorite) next.add(key); else next.delete(key);
            return next;
        });
    };

    if (results.length === 0) {
        return (
            <div className="container mx-auto p-4 max-w-2xl">
                <p className="text-sm text-gray-600">検索結果がありません。</p>
                <Link to="/" className="mt-2 inline-block text-blue-600 underline">
                    まな板に戻る
                </Link>
            </div>
        );
    }

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="bg-white shadow-md rounded-lg p-6">
                <h1 className="text-2xl font-bold text-center mb-4">検索結果</h1>
                <Link to="/" className="mb-4 inline-block text-blue-600 underline">
                    まな板に戻る
                </Link>
                <Link to="/favorites" className="mb-4 ml-4 inline-block text-blue-600 underline">
                    お気に入りを見る
                </Link>

                {results.map((result) => (
                    <section key={result.ingredient} className="mb-6">
                        <h2 className="text-lg font-semibold mb-2">{result.ingredient}</h2>

                        {result.rakutenRecipes.length > 0 && (
                            <div className="mb-3">
                                <h3 className="text-sm font-semibold text-gray-600 mb-2">レシピ</h3>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                    {result.rakutenRecipes.map((recipe) => (
                                        <div key={recipe.recipeId} className="rounded-md border bg-gray-50 p-3">
                                            <div className="flex items-start justify-between gap-2">
                                                <h4 className="font-semibold">{recipe.title}</h4>
                                                <FavoriteButton
                                                    item={{
                                                        kind: "recipe",
                                                        item_id: recipe.recipeId,
                                                        title: recipe.title,
                                                        description: recipe.description,
                                                        url: recipe.url,
                                                        image_url: recipe.imageUrl,
                                                    }}
                                                    userId={DEMO_USER_ID}
                                                    isFavorite={favoriteKeys.has(`recipe:${recipe.recipeId}`)}
                                                    onChange={(nowFavorite) => toggleKey(`recipe:${recipe.recipeId}`, nowFavorite)}
                                                />
                                            </div>
                                            <p className="text-sm text-gray-600">{recipe.description}</p>
                                            {recipe.imageUrl && (
                                                <img
                                                    src={recipe.imageUrl}
                                                    alt={recipe.title}
                                                    className="mt-2 h-36 w-full object-cover rounded"
                                                />
                                            )}
                                            <a
                                                href={recipe.url}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="mt-2 inline-block text-blue-600 underline"
                                            >
                                                レシピを見る
                                            </a>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {result.youtubeVideos.length > 0 && (
                            <div>
                                <h3 className="text-sm font-semibold text-gray-600 mb-2">動画</h3>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                    {result.youtubeVideos.map((video) => (
                                        <div key={video.videoId} className="rounded-md border bg-gray-50 p-3">
                                            <div className="flex items-start justify-between gap-2">
                                                <h4 className="font-semibold">{video.title}</h4>
                                                <FavoriteButton
                                                    item={{
                                                        kind: "video",
                                                        item_id: video.videoId,
                                                        title: video.title,
                                                        description: video.description,
                                                        url: video.url,
                                                        image_url: video.thumbnailUrl,
                                                    }}
                                                    userId={DEMO_USER_ID}
                                                    isFavorite={favoriteKeys.has(`video:${video.videoId}`)}
                                                    onChange={(nowFavorite) => toggleKey(`video:${video.videoId}`, nowFavorite)}
                                                />
                                            </div>
                                            <p className="text-sm text-gray-600 line-clamp-2">{video.description}</p>
                                            {video.thumbnailUrl && (
                                                <img
                                                    src={video.thumbnailUrl}
                                                    alt={video.title}
                                                    className="mt-2 h-36 w-full object-cover rounded"
                                                />
                                            )}
                                            <a
                                                href={video.url}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="mt-2 inline-block text-blue-600 underline"
                                            >
                                                動画を見る
                                            </a>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}

                        {result.rakutenRecipes.length === 0 && result.youtubeVideos.length === 0 && (
                            <p className="text-sm text-gray-500">該当するレシピ・動画は見つかりませんでした。</p>
                        )}
                    </section>
                ))}
            </div>
        </div>
    );
};

export default Result;
