export type RecipeType = {
  recipeId: string;
  recipeTitle: string;
  recipeDescription: string;
  recipeUrl: string;
  foodImageUrl: string;
  materials: string[];
};

export type RecipeSearchResult = {
  source: string;
  total: number;
  items: Array<{
    recipe_id: string;
    title: string;
    description: string;
    url: string;
    image_url: string | null;
    materials: string[];
  }>;
};
