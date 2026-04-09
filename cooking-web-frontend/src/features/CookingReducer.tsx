/**
 * 食材の状態管理
 * 食材を追加する画面・検索画面・詳細画面で使用する
 */

import { State, Action } from "../types/ingredient";

const CookingReducer = (state: State, action: Action) => {
    switch (action.type) {
        // 食材を追加する
        case "ADD_INGREDIENT":
            return {
                ...state,
                ingredients: [...state.ingredients, { name: action.payload, quantity: "中" }],
            }
        // 食材を削除する
        case "REMOVE_INGREDIENT":
            return {
                ...state,
                ingredients: state.ingredients.filter(
                    (ingredient) => ingredient.name !== action.payload
                ),
            }
        // 追加した食材をもとにレシピを検索する
        case "SET_SEARCH_QUERY":
            return {
                ...state,
                searchQuery: action.payload,
            }
        // 検索結果を表示する
        case "SEARCH_RECIPES":
            return {
                ...state,
                searchResults: state.ingredients.filter((ingredient) =>
                    ingredient.name.includes(state.searchQuery)
                ),
            }
        default:
            return state;
    }
}

export default CookingReducer;
