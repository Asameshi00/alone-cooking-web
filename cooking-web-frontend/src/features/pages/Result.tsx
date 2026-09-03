/**
 * まな板の食材で検索したレシピ・動画の一覧を表示する画面
 */

import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { IngredientSearchResult } from '../../types/recipe';

interface ResultLocationState {
    results?: IngredientSearchResult[];
}

const Result: React.FC = () => {
    const location = useLocation();
    const results = (location.state as ResultLocationState | null)?.results ?? [];

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

                {results.map((result) => (
                    <section key={result.ingredient} className="mb-6">
                        <h2 className="text-lg font-semibold mb-2">{result.ingredient}</h2>

                        {result.rakutenRecipes.length > 0 && (
                            <div className="mb-3">
                                <h3 className="text-sm font-semibold text-gray-600 mb-2">レシピ</h3>
                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                                    {result.rakutenRecipes.map((recipe) => (
                                        <div key={recipe.recipeId} className="rounded-md border bg-gray-50 p-3">
                                            <h4 className="font-semibold">{recipe.title}</h4>
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
                                            <h4 className="font-semibold">{video.title}</h4>
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
