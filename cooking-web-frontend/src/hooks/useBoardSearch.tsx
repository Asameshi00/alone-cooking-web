import { useCallback, useState } from "react";
import { BoardSearchResultRaw, IngredientSearchResult } from "../types/recipe";

interface FetchOptions {
  limit?: number;
}

interface UseBoardSearchReturn {
  results: IngredientSearchResult[];
  loading: boolean;
  error: string | null;
  searchRecipes: (ingredientNames: string[], options?: FetchOptions) => Promise<IngredientSearchResult[]>;
}

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ?? "http://localhost:8000/api/v1";

// まな板の食材から楽天レシピ・YouTube動画をまとめて検索するフック
export const useBoardSearch = (): UseBoardSearchReturn => {
  const [results, setResults] = useState<IngredientSearchResult[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const searchRecipes = useCallback(async (ingredientNames: string[], options: FetchOptions = {}) => {
    if (ingredientNames.length === 0) {
      setError("食材を1つ以上まな板に追加してください。");
      setResults([]);
      return [];
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/board/search`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ingredient_names: ingredientNames,
          limit: options.limit ?? 10,
        }),
      });

      if (!response.ok) {
        throw new Error(`バックエンドAPIリクエストに失敗しました: ${response.status}`);
      }

      const data: BoardSearchResultRaw = await response.json();
      const formattedResults: IngredientSearchResult[] = data.results.map((result) => ({
        ingredient: result.ingredient,
        rakutenRecipes: result.rakuten_recipes.map((recipe) => ({
          recipeId: recipe.recipe_id,
          title: recipe.title,
          description: recipe.description,
          url: recipe.url,
          imageUrl: recipe.image_url,
          materials: recipe.materials,
        })),
        youtubeVideos: result.youtube_videos.map((video) => ({
          videoId: video.video_id,
          title: video.title,
          description: video.description,
          url: video.url,
          thumbnailUrl: video.thumbnail_url,
        })),
      }));

      setResults(formattedResults);
      return formattedResults;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "不明なエラーが発生しました";
      setError(errorMessage);
      setResults([]);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  return { results, loading, error, searchRecipes };
};

export default useBoardSearch;
