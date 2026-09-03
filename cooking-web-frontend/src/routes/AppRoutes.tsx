// ルーティング設定

import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import App from '../App';
import Result from '../features/pages/Result';

const AppRoutes: React.FC = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<App />} />
                <Route path="/result" element={<Result />} />
                <Route path="/recipe" element={<div>レシピ一覧</div>} />
                <Route path="/recipe/:id" element={<div>レシピ詳細</div>} />
            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;
