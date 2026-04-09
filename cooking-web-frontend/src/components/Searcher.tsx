import React from "react";
import { useAiSuggestion } from "../hooks/useAiSuggestion";
import { useRakutenAPI } from "../hooks/useRakuten";
import { Ingredient } from "../types/ingredient";

/** 検索のプロパティ **/
interface SearcherProps {
    ingredients: Ingredient[];
}

const Searcher: React.FC<SearcherProps> = ({ ingredients }) => {
    const { recipes, loading, error, fetchRecipes } = useRakutenAPI();
    const {
        suggestion,
        loading: aiLoading,
        error: aiError,
        fetchSuggestion
    } = useAiSuggestion();

    // 検索ボタンを押したときの処理
    const handleSearch = async () => {
        const ingredient = ingredients.map(ingredient => ingredient.name);
        await fetchRecipes(ingredient, {
            hits: 20,
        })
    };

    const handleAiSuggest = async () => {
        const ingredient = ingredients.map((item) => item.name);
        await fetchSuggestion(ingredient);
    };

    return (
        <div className="mb-4">
            <div className="flex gap-2">
                <button
                    onClick={handleSearch}
                    className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    disabled={loading}
                >
                    {loading ? "検索中..." : "レシピ検索"}
                </button>
                <button
                    onClick={handleAiSuggest}
                    className="mt-2 px-4 py-2 bg-emerald-500 text-white rounded-md hover:bg-emerald-600 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    disabled={aiLoading}
                >
                    {aiLoading ? "提案中..." : "AI提案"}
                </button>
            </div>

            {error && <div className="mt-2 text-red-500">エラーが発生しました: {error}</div>}
            {aiError && <div className="mt-2 text-red-500">AIエラー: {aiError}</div>}

            {recipes.map((recipe, index) => (
                <div key={recipe.recipeId || index} className="mt-3 rounded-md border bg-gray-50 p-3">
                    <h3 className="font-semibold">{recipe.recipeTitle}</h3>
                    <p className="text-sm text-gray-600">{recipe.recipeDescription}</p>
                    <img src={recipe.foodImageUrl} alt={recipe.recipeTitle} className="mt-2 h-36 w-full object-cover rounded" />
                    <a href={recipe.recipeUrl} target="_blank" rel="noreferrer" className="mt-2 inline-block text-blue-600 underline">
                        レシピを見る
                    </a>
                </div>
            ))}

            {suggestion && (
                <div className="mt-4 rounded-md border bg-emerald-50 p-3">
                    <p className="text-xs text-gray-500">provider: {suggestion.provider}</p>
                    <h3 className="font-semibold">{suggestion.recipe_title}</h3>
                    <p className="text-sm">{suggestion.recipe_description}</p>
                    <p className="mt-2 font-medium">手順</p>
                    <ol className="list-decimal pl-5 text-sm">
                        {suggestion.steps.map((step, idx) => (
                            <li key={idx}>{step}</li>
                        ))}
                    </ol>
                    <p className="mt-2 font-medium">コツ</p>
                    <ul className="list-disc pl-5 text-sm">
                        {suggestion.tips.map((tip, idx) => (
                            <li key={idx}>{tip}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
}

export default Searcher;
