/** 食品の量の型定義 **/
type Quantity = '多' | '中' | '少' ;

/** 食材の型定義 **/
interface Ingredient {
    name: string;
    quantity: Quantity;
}

/** Webサイトの状態管理 **/
interface State {
    ingredients: Ingredient[];
    searchQuery: string;
    searchResults: Ingredient[];
}

/** アクションの型定義 **/
type Action =
    | { type: 'ADD_INGREDIENT'; payload: string }
    | { type: 'REMOVE_INGREDIENT'; payload: string }
    | { type: 'SET_SEARCH_QUERY'; payload: string }
    | { type: 'SEARCH_RECIPES' };

export type { Quantity, Ingredient, State, Action };