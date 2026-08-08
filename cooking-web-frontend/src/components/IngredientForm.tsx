/**
 * テキストバーで食材を追加するコンポーネント
 */

import React, { useState, useCallback } from 'react';

/** 食材追加のプロパティ **/
interface IngredientFormProps {
    addIngredient: (ingredient: string) => boolean;
}

const IngredientForm: React.FC<IngredientFormProps> = ({ addIngredient }) => {
    const [ingredientName, setIngredientName] = useState<string>('');
    const [errorMessage, setErrorMessage] = useState<string>('');

    const handleNameChange = useCallback((event: React.ChangeEvent<HTMLInputElement>) => {
        setIngredientName(event.target.value);
        // 入力時にエラーメッセージをクリア
        setErrorMessage('');
    }, []);

    const handleSubmit = useCallback((event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (ingredientName.trim()) {
            const isAdded = addIngredient(ingredientName.trim());
            if (isAdded) {
                // 追加成功時はフォームをクリア
                setIngredientName('');
                setErrorMessage('');
            } else {
                // 重複時はエラーメッセージを表示
                setErrorMessage('この食材は既に追加されています');
            }
        }
    }, [ingredientName, addIngredient]);


    return (
        <div>
            <form onSubmit={handleSubmit} className="flex gap-3 mb-4">
                <div>
                    <input
                        type="text"
                        value={ingredientName}
                        onChange={handleNameChange}
                        placeholder="食材を追加"
                        className="flex-grow px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                </div>

                <button
                    type="submit"
                    className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                    追加
                </button>
            </form>
            {errorMessage && (
                <p className="text-red-500 text-sm mt-2">{errorMessage}</p>
            )}
        </div>
    );
};

export default IngredientForm;
