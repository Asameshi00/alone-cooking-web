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
            </div>

            {error && <div className="mt-2 text-red-500">エラーが発生しました: {error}</div>}

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

        </div>
    );
}

export default Searcher;
