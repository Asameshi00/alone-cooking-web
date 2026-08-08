/**
 * まな板UIコンポーネント
 * 食材リストからドラッグアンドドロップされた食材を保持し、検索対象とする
 */

import React, { useCallback, useState } from 'react';
import { Ingredient } from '../types/ingredient';

/** まな板のプロパティ **/
interface CuttingBoardProps {
    boardIngredients: Ingredient[];
    addToBoard: (ingredient: Ingredient) => void;
    removeFromBoard: (name: string) => void;
}

const CuttingBoard: React.FC<CuttingBoardProps> = ({
    boardIngredients,
    addToBoard,
    removeFromBoard,
}) => {
    const [isDragOver, setIsDragOver] = useState(false);

    const handleDragOver = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setIsDragOver(true);
    }, []);

    const handleDragLeave = useCallback(() => {
        setIsDragOver(false);
    }, []);

    const handleDrop = useCallback((event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        setIsDragOver(false);
        const data = event.dataTransfer.getData('application/json');
        if (!data) {
            return;
        }
        const ingredient: Ingredient = JSON.parse(data);
        addToBoard(ingredient);
    }, [addToBoard]);

    return (
        <div className="mb-6">
            <h2 className="text-lg font-semibold mb-2">まな板</h2>
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`min-h-[120px] rounded-lg border-2 border-dashed p-4 transition-colors ${
                    isDragOver ? 'border-blue-500 bg-blue-50' : 'border-amber-400 bg-amber-50'
                }`}
            >
                {boardIngredients.length === 0 ? (
                    <p className="text-sm text-gray-500 text-center">
                        下の食材リストからドラッグ＆ドロップして追加してください
                    </p>
                ) : (
                    <div className="flex flex-wrap gap-2">
                        {boardIngredients.map((ingredient) => (
                            <span
                                key={ingredient.name}
                                className="flex items-center gap-2 px-3 py-1 bg-white rounded-full shadow-sm border border-amber-300"
                            >
                                <span className="text-gray-700">{ingredient.name}</span>
                                <button
                                    onClick={() => removeFromBoard(ingredient.name)}
                                    className="text-red-500 hover:text-red-700 focus:outline-none"
                                    aria-label={`${ingredient.name}をまな板から削除`}
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default CuttingBoard;
