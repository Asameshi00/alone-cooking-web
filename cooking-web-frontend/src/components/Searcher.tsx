import React from "react";
import { useNavigate } from "react-router-dom";
import { useBoardSearch } from "../hooks/useBoardSearch";
import { Ingredient } from "../types/ingredient";

/** 検索のプロパティ **/
interface SearcherProps {
    ingredients: Ingredient[];
}

const Searcher: React.FC<SearcherProps> = ({ ingredients }) => {
    const { loading, error, searchRecipes } = useBoardSearch();
    const navigate = useNavigate();

    // 検索ボタンを押したときの処理。検索後は結果画面へ遷移する
    const handleSearch = async () => {
        const ingredientNames = ingredients.map(ingredient => ingredient.name);
        const results = await searchRecipes(ingredientNames);
        if (results.length > 0) {
            navigate("/result", { state: { results } });
        }
    };

    return (
        <div className="mb-4">
            <div className="flex gap-2">
                <button
                    onClick={handleSearch}
                    className="mt-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    disabled={loading || ingredients.length === 0}
                >
                    {loading ? "検索中..." : "まな板の食材で検索"}
                </button>
            </div>

            {error && <div className="mt-2 text-red-500">エラーが発生しました: {error}</div>}
        </div>
    );
}

export default Searcher;
