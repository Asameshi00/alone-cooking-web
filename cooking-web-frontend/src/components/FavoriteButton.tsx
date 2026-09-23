import React, { useState } from "react";
import { useFavorites } from "../hooks/useFavorites";
import { FavoriteItem } from "../types/favorite";

// お気に入りボタンのpropsの型定義
interface FavoriteButtonProps {
    item: FavoriteItem;
    userId: number;
    isFavorite: boolean;
    onChange: (nowFavorite: boolean) => void;
}

const FavoriteButton: React.FC<FavoriteButtonProps> = ({ item, userId, isFavorite, onChange }) => {
    const { addFavorite, removeFavorite } = useFavorites();
    const [busy, setBusy] = useState<boolean>(false);

    const handleClick = async () => {
        // ボタンが押されている場合は処理を返す
        if (busy) return;

        setBusy(true);
        // お気に入りが追加されている場合は解除する
        if (isFavorite) {
            // お気に入りが解除されている場合は追加する
            const ok = await removeFavorite(item.item_id, item.kind, userId);
            if (ok) onChange(false);
        } else {
            const favorite = await addFavorite(item, userId);
            if (favorite) onChange(true);
        }
    setBusy(false);
    };

return (
    <button
        type="button"
        onClick={handleClick}
        disabled={busy}
        aria-label={isFavorite ? "お気に入りから削除" : "お気に入りに追加"}
        aria-pressed={isFavorite}
        className="text-amber-500 hover:text-amber-600 text-xl leading-none focus:outline-none focus:ring-2 focus:ring-amber-400 disabled:opacity-50"
    >
        {isFavorite ? "★" : "☆"}
    </button>
    );
};

export default FavoriteButton;
