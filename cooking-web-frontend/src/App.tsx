import React, { useCallback, useState } from "react";
import IngredientForm from "./components/IngredientForm";
import IngredientList from "./components/InventoryList";
import CuttingBoard from "./components/CuttingBoard";
import { Ingredient } from "./types/ingredient";
import Searcher from "./components/Searcher";

const App: React.FC = () => {
    const [ingredients, setIngredients] = useState<Ingredient[]>([]);
    const [boardIngredients, setBoardIngredients] = useState<Ingredient[]>([]);

    // 戻り値: 追加成功時はtrue、重複時はfalse
    const addIngredient = useCallback((name: string): boolean => {
        let isAdded = false;
        setIngredients((prevIngredients) => {
            const isDuplicate = prevIngredients.some(
                (ingredient) => ingredient.name.toLowerCase() === name.toLowerCase());
            if (!isDuplicate) {
                isAdded = true;
                return [...prevIngredients, { name: name }];
            }
            return prevIngredients;
        });
        return isAdded;
    }, []);

    // filterメソッドを使用して、指定された食材を除外した新しい配列を作成
    const removeIngredient = useCallback((ingredientName: string) => {
        setIngredients((prevIngredients) => prevIngredients.filter((ingredient) => ingredient.name !== ingredientName));
    }, []);

    // まな板に食材を追加する（重複時は追加しない）
    const addToBoard = useCallback((ingredient: Ingredient) => {
        setBoardIngredients((prevBoardIngredients) => {
            const isDuplicate = prevBoardIngredients.some(
                (boardIngredient) => boardIngredient.name.toLowerCase() === ingredient.name.toLowerCase());
            if (isDuplicate) {
                return prevBoardIngredients;
            }
            return [...prevBoardIngredients, ingredient];
        });
    }, []);

    // まな板から食材を取り除く
    const removeFromBoard = useCallback((ingredientName: string) => {
        setBoardIngredients((prevBoardIngredients) =>
            prevBoardIngredients.filter((ingredient) => ingredient.name !== ingredientName));
    }, []);

    return (
        <div className="container mx-auto p-4 max-w-2xl">
            <div className="bg-white shadow-md rounded-lg p-6">
                <h1 className="text-2xl font-bold text-center mb-4">Cooking-Web</h1>
                <p className="mb-4 text-center text-sm text-gray-600">
                    食材からレシピ検索を行います
                </p>
                <CuttingBoard
                    boardIngredients={boardIngredients}
                    addToBoard={addToBoard}
                    removeFromBoard={removeFromBoard}
                />
                <Searcher ingredients={boardIngredients} />
                <IngredientForm addIngredient={addIngredient} />
                <IngredientList ingredients={ingredients} removeIngredient={removeIngredient} />
            </div>
        </div>
    );
};

export default App;
