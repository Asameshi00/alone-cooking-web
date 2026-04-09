import { useCallback, useState } from "react";
import { RecipeSearchResult, RecipeType } from "../types/recipe";

interface FetchOptions {
  hits?: number;
}

interface UseRakutenReturn {
  recipes: RecipeType[];
  loading: boolean;
  error: string | null;
  fetchRecipes: (ingredients: string[], options?: FetchOptions) => Promise<void>;
}

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const useRakutenAPI = (): UseRakutenReturn => {
  const [recipes, setRecipes] = useState<RecipeType[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRecipes = useCallback(async (ingredients: string[], options: FetchOptions = {}) => {
    if (ingredients.length === 0) {
      setError("食材を1つ以上追加してください。");
      setRecipes([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const keyword = ingredients.join(" ");
      const params = new URLSearchParams({
        ingredient: keyword,
        limit: String(options.hits ?? 20),
      });

      const response = await fetch(`${API_BASE_URL}/recipes/search?${params.toString()}`);
      if (!response.ok) {
        throw new Error(`バックエンドAPIリクエストに失敗しました: ${response.status}`);
      }

      const data: RecipeSearchResult = await response.json();
      const formattedRecipes: RecipeType[] = data.items.map((item) => ({
        recipeId: item.recipe_id,
        recipeTitle: item.title,
        recipeDescription: item.description,
        recipeUrl: item.url,
        foodImageUrl: item.image_url ?? "/default-recipe-image.jpg",
        materials: item.materials ?? [],
      }));

      setRecipes(formattedRecipes);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "不明なエラーが発生しました";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  return { recipes, loading, error, fetchRecipes };
};

export default useRakutenAPI;
