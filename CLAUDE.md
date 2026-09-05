# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

cooking-web is a two-part app: leftover ingredients go in, recipe/video suggestions come out. Backend is FastAPI (`cooking-web-backend`), frontend is React + TypeScript via Create React App (`cooking-web-frontend`). Recipes come from the Rakuten Recipe API, cooking videos from the YouTube Data API v3.

## Commands

Run all commands below from the repo root via `make`, or `cd` into the relevant directory and run the underlying command directly.

```bash
make install          # install both frontend and backend deps
make run-frontend      # cd cooking-web-frontend && npm start        (port 3000)
make run-backend       # cd cooking-web-backend && uv run uvicorn app.main:app --reload --port 8000
make build             # cd cooking-web-frontend && npm run build
make test              # cd cooking-web-frontend && npm test
make lint              # lints both frontend (eslint) and backend (ruff)
make lint-frontend     # cd cooking-web-frontend && npm run lint
make lint-backend      # cd cooking-web-backend && uv run ruff check app
```

Backend-specific (no test files exist yet, but `pytest` and the `test/` tree — mirroring `app/{api,core,db,schemas,services}` — are already set up):

```bash
cd cooking-web-backend
uv sync                                    # install deps
uv run uvicorn app.main:app --reload --port 8000
uv run ruff check app
uv run pytest                              # run backend tests
uv run pytest test/api/test_board.py -k some_case   # run a single test, once tests exist
```

Frontend single-test runs (CRA/Jest):

```bash
cd cooking-web-frontend
npm test -- --testPathPattern=Searcher     # run tests matching a file/name
```

Docker Compose (Postgres instead of the backend's default SQLite) is available at the repo root: `docker-compose.yml` spins up `db` (Postgres 16), `backend`, `frontend`, and `pgadmin`.

## Environment variables

Backend reads `.env` in `cooking-web-backend/` (via `pydantic-settings`):

```
RAKUTEN_APP_ID=...
RAKUTEN_AFFILIATE_ID=...
YOUTUBE_API_KEY=...
DATABASE_URL=sqlite+aiosqlite:///./app.db      # optional, defaults to local SQLite
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173   # optional
APP_ENV=dev                                    # optional
```

Frontend reads `REACT_APP_API_BASE_URL` (defaults to `http://localhost:8000/api/v1`), set in `cooking-web-frontend/.env`.

**Note:** `ALLOWED_ORIGINS` defaults to Vite's port (5173), but the frontend actually runs on CRA's default port 3000 — CORS will reject requests unless this is overridden.

## Backend architecture (`cooking-web-backend`)

Layered: `app/api` (FastAPI routers, controller layer) → `app/services` (business logic, external API calls) → `app/models` (SQLAlchemy 2.0 async ORM) / `app/db` (session + init). `app/schemas` holds Pydantic request/response models, kept separate from ORM models.

- All endpoints are mounted under `api_prefix` (`/api/v1`) in `app/main.py`, which also wires CORS and runs `init_db()` on startup (creates tables and seeds a demo user with email `demo@example.com`).
- There is no auth layer yet — endpoints take `user_id` as a plain query/body param, resolved against the seeded demo user.
- The core domain flow is **inventory → board → search**, implemented across `app/api/inventory.py` and `app/api/board.py`:
  1. `POST /api/v1/inventory` — add an ingredient to a user's inventory (persisted, `InventoryItem` model).
  2. `POST /api/v1/board/ingredients` — given `inventory_ids`, resolve them to ingredient name strings (`BoardService.fetch_ingredient_names`).
  3. `POST /api/v1/board/search` — given ingredient name strings directly (no DB lookup), fan out per-ingredient to `RakutenRecipeService` and `YouTubeRecipeService` concurrently via `asyncio.gather` (`BoardService.search_recipes_from_board`), returning recipes + videos grouped by ingredient.
- `RakutenRecipeService` maps an ingredient name to a Rakuten recipe category by fuzzy-matching against a cached category dataframe (`CategoryList` API, cached at class level on first fetch), then queries `CategoryRanking` for that category.
- Favorites (`app/api/favorites.py`) are a separate simple CRUD keyed by `user_id`.
- See `cooking-web-backend/README.md` for the full endpoint table and a mermaid diagram of the inventory→board→search flow.

## Frontend architecture (`cooking-web-frontend`)

React 19 + TypeScript, Tailwind for styling, `react-router-dom` for routing (`src/routes/AppRoutes.tsx`, rendered from `src/index.tsx`).

- **State is local, not wired to the backend inventory API.** `App.tsx` holds two in-memory arrays via `useState`: `ingredients` (everything the user has typed into `IngredientForm`, shown as a gallery in `InventoryList`) and `boardIngredients` (the subset dragged onto the `CuttingBoard`). Nothing is persisted to `/api/v1/inventory` — despite that endpoint existing on the backend, the frontend doesn't call it. Be aware of this gap before assuming frontend and backend are in sync.
- Drag-and-drop from the ingredient gallery (`InventoryList`) onto the `CuttingBoard` uses the native HTML5 DnD API (`draggable`, `dataTransfer`), not a library.
- Search flow: `Searcher` calls `useBoardSearch` (POSTs `boardIngredients` names to `/api/v1/board/search`), then on success navigates to `/result` via `react-router-dom`, passing results through router `state` (not a global store) — read back with `useLocation().state` in `features/pages/Result.tsx`. There is currently no fallback for a page refresh on `/result` (state is lost; the page shows an empty-results message).
- Hooks under `src/hooks` follow one pattern: wrap a `fetch` to `${REACT_APP_API_BASE_URL}/...`, expose `{ data, loading, error, fetchX }`, and convert the backend's snake_case JSON into camelCase types (see `useBoardSearch.tsx` and its `BoardSearchResultRaw` → `IngredientSearchResult` mapping in `types/recipe.ts`).
- `useAiSuggestion.tsx` and `useYoutube.tsx`/`useGemini.tsx` are leftover/unused — the AI-suggestion feature and a standalone YouTube hook were removed from the UI but the hook files (and `types/ai.ts`) weren't deleted.
- `src/features/CookingReducer.tsx` (a `useReducer`-style reducer over `State`/`Action` in `types/ingredient.ts`) is also dead code — not wired into `App.tsx`, which manages state with plain `useState` instead.
- `src/stores` and `src/schemas` directories exist but are currently empty.
