import { useCallback, useState } from "react";
import { AISuggestion } from "../types/ai";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL ?? "http://localhost:8000/api/v1";

interface UseAiSuggestionReturn {
  suggestion: AISuggestion | null;
  loading: boolean;
  error: string | null;
  fetchSuggestion: (leftovers: string[]) => Promise<void>;
}

export const useAiSuggestion = (): UseAiSuggestionReturn => {
  const [suggestion, setSuggestion] = useState<AISuggestion | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSuggestion = useCallback(async (leftovers: string[]) => {
    if (leftovers.length === 0) {
      setError("食材を1つ以上追加してください。");
      setSuggestion(null);
      return;
    }

    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_BASE_URL}/ai/suggest`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          leftovers,
          bargain_items: [],
        }),
      });

      if (!response.ok) {
        throw new Error(`AI提案APIリクエストに失敗しました: ${response.status}`);
      }

      const data: AISuggestion = await response.json();
      setSuggestion(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "不明なエラーが発生しました";
      setError(errorMessage);
      setSuggestion(null);
    } finally {
      setLoading(false);
    }
  }, []);

  return { suggestion, loading, error, fetchSuggestion };
};
