export type RakutenRecipe = {
  recipeId: string;
  title: string;
  description: string;
  url: string;
  imageUrl: string | null;
  materials: string[];
};

export type YoutubeVideo = {
  videoId: string;
  title: string;
  description: string;
  url: string;
  thumbnailUrl: string | null;
};

/** 1つの食材に対するレシピ・動画の検索結果 **/
export type IngredientSearchResult = {
  ingredient: string;
  rakutenRecipes: RakutenRecipe[];
  youtubeVideos: YoutubeVideo[];
};

/** まな板APIレスポンスの生データ（バックエンドのsnake_case） **/
export type BoardSearchResultRaw = {
  results: Array<{
    ingredient: string;
    rakuten_recipes: Array<{
      recipe_id: string;
      title: string;
      description: string;
      url: string;
      image_url: string | null;
      materials: string[];
    }>;
    youtube_videos: Array<{
      video_id: string;
      title: string;
      description: string;
      url: string;
      thumbnail_url: string | null;
    }>;
  }>;
};
