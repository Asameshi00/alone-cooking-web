/**
 * 追加した食材のリストをギャラリー形式で表示するコンポーネント
 * カードはドラッグしてまな板へ追加できる
 */

import React, { useCallback } from 'react';
import { Ingredient } from '../types/ingredient';

/** 食材リストのインタフェース **/
interface InventoryListProps {
    ingredients: Ingredient[];
    removeIngredient: (ingredient: string) => void;
}

const InventoryList: React.FC<InventoryListProps> = ({ ingredients, removeIngredient }) => {
    const handleDragStart = useCallback((event: React.DragEvent<HTMLDivElement>, ingredient: Ingredient) => {
        event.dataTransfer.setData('application/json', JSON.stringify(ingredient));
        event.dataTransfer.effectAllowed = 'copy';
    }, []);

    if (ingredients.length === 0) {
        return <p className="text-sm text-gray-500">まだ在庫に食材が追加されていません。</p>;
    }

    return (
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
            {ingredients.map((ingredient) => (
                <div
                    key={ingredient.name}
                    draggable
                    onDragStart={(event) => handleDragStart(event, ingredient)}
                    className="flex flex-col items-center gap-1 p-3 bg-gray-100 rounded-md cursor-grab active:cursor-grabbing hover:shadow-md transition-shadow"
                >
                    <span className="text-gray-700 font-medium">{ingredient.name}</span>
                    <button
                        onClick={() => removeIngredient(ingredient.name)}
                        className="mt-1 px-2 py-1 text-xs bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
                    >
                        削除
                    </button>
                </div>
            ))}
        </div>
    );
};

export default InventoryList;
