import React, { useCallback, useState } from "react";
import IngredientForm from "./components/IngredientForm";
import IngredientList from "./components/IngredientList";
import { Ingredient, Quantity } from "./types/ingredient";
import Searcher from "./components/Searcher";

const App: React.FC = () => {
    const [ingredients, setIngredients] = useState<Ingredient[]>([]);

    // 戻り値: 追加成功時はtrue、重複時はfalse
    const addIngredient = useCallback((name: string, quantity: Quantity): boolean => {
        let isAdded = false;
        setIngredients((prevIngredients) => {
            const isDuplicate = prevIngredients.some(
                (ingredient) => ingredient.name.toLowerCase() === name.toLowerCase());
            if (!isDuplicate) {
                isAdded = true;
                return [...prevIngredients, { name: name, quantity: quantity }];
            }
            return prevIngredients;
        });
        return isAdded;
    }, []);

    // filterメソッドを使用して、指定された食材を除外した新しい配列を作成
    const removeIngredient = useCallback((ingredientName: string) => {
        setIngredients((prevIngredients) => prevIngredients.filter((ingredient) => ingredient.name !== ingredientName));
    }, []);

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="bg-white shadow-md rounded-lg p-6">
                <h1 className="text-2xl font-bold text-center mb-4">Cooking-Web</h1>
                <p className="mb-4 text-center text-sm text-gray-600">
                    余り物の食材から、レシピ検索とAI提案を行います。
                </p>
                <Searcher ingredients={ingredients} />
                <IngredientForm addIngredient={addIngredient} />
                <IngredientList ingredients={ingredients} removeIngredient={removeIngredient} />
            </div>
        </div>
    );
};

export default App;
