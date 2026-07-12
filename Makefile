FRONTEND_DIR = cooking-web-frontend
BACKEND_DIR = cooking-web-backend

.PHONY: help
help:
	@echo "使用可能なコマンド"
	@echo "  run              : フロントとバックエンドを個別に起動方法表示"
	@echo "  run-frontend     : フロントエンドを起動"
	@echo "  run-backend      : バックエンドを起動"
	@echo "  build            : フロントエンドをビルド"
	@echo "  test             : フロントエンドのテストを実行"
	@echo "  lint             : フロントとバックエンドのlintを実行"
	@echo "  lint-frontend    : フロントエンドのリント"
	@echo "  lint-backend     : バックエンドのリント"
	@echo "  install          : フロント/バックエンドの依存関係をインストール"
	@echo "  install-frontend : フロントエンド依存をインストール"
	@echo "  install-backend  : バックエンド依存をインストール(uv sync)"
	@echo "  clean-frontend   : フロントの依存関係をクリーンアップ"
	@echo "  clean-backend    : バックエンドのキャッシュをクリーンアップ"
	@echo "  list             : フロントエンド依存を表示"
	@echo "  check-old        : フロントの古い依存を表示"
	@echo "  check-unused     : フロントの未使用依存を表示"
	@echo "  update           : フロント依存を更新"
	@echo "  audit            : フロント依存を監査"

.PHONY: run
run:
	@echo "別ターミナルで以下を実行してください:"
	@echo "  make run-frontend"
	@echo "  make run-backend"

.PHONY: run-frontend
run-frontend:
	@echo "=== フロントエンドを起動 ==="
	cd $(FRONTEND_DIR) && npm start

.PHONY: run-backend
run-backend:
	@echo "=== バックエンドを起動 ==="
	cd $(BACKEND_DIR) && uv run uvicorn app.main:app --reload --port 8000

.PHONY: build
build:
	@echo "=== フロントエンドのビルド ==="
	cd $(FRONTEND_DIR) && npm run build
	@echo "Build complete."

.PHONY: test
test:
	@echo "=== フロントエンドのテスト ==="
	cd $(FRONTEND_DIR) && npm test
	@echo "Test complete."

.PHONY: install
install: install-frontend install-backend
	@echo "Install complete."

.PHONY: install-frontend
install-frontend:
	@echo "=== フロントエンド依存のインストール ==="
	@if [ "$(filter-out $@ install,$(MAKECMDGOALS))" != "" ]; then \
		echo "Installing packages: $(filter-out $@ install,$(MAKECMDGOALS))"; \
		cd $(FRONTEND_DIR) && npm install $(filter-out $@ install,$(MAKECMDGOALS)); \
	else \
		echo "Installing all frontend dependencies"; \
		cd $(FRONTEND_DIR) && npm install; \
	fi

.PHONY: install-backend
install-backend:
	@echo "=== バックエンド依存のインストール ==="
	cd $(BACKEND_DIR) && uv sync

.PHONY: uninstall
uninstall:
	@echo "=== フロントエンド依存のアンインストール ==="
	@if [ "$(filter-out $@,$(MAKECMDGOALS))" != "" ]; then \
		echo "Uninstalling packages: $(filter-out $@,$(MAKECMDGOALS))"; \
		cd $(FRONTEND_DIR) && npm uninstall $(filter-out $@,$(MAKECMDGOALS)); \
	else \
		echo "Package名を指定してください: make uninstall <package>"; \
	fi

.PHONY: clean-frontend
clean-frontend:
	@echo "=== フロントエンド依存をクリーンアップ ==="
	cd $(FRONTEND_DIR) && npm prune && npm cache clean --force
	@echo "Clean complete."

.PHONY: clean-backend
clean-backend:
	@echo "=== バックエンド依存をクリーンアップ ==="
	cd $(BACKEND_DIR) && uv clean
	cd $(BACKEND_DIR) && rm -rf __pycache__
	cd $(BACKEND_DIR) && rm -rf app/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/models/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/schemas/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/services/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/core/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/db/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/api/__pycache__
	cd $(BACKEND_DIR) && rm -rf app/main.pyc
	@echo "Clean complete."

.PHONY: lint
lint:
	@echo "=== フロントエンド lint ==="
	cd $(FRONTEND_DIR) && npm run lint
	@echo "=== バックエンド lint ==="
	cd $(BACKEND_DIR) && uv run ruff check app
	@echo "Lint complete."

.PHONY: lint-frontend
lint-frontend:
	@echo "=== フロントエンド lint ==="
	cd $(FRONTEND_DIR) && npm run lint
	@echo "Lint complete."

.PHONY: lint-backend
lint-backend:
	@echo "=== バックエンド lint ==="
	cd $(BACKEND_DIR) && uv run ruff check app
	@echo "Lint complete."

.PHONY: check-old
check-old:
	@echo "=== フロントエンドの古い依存 ==="
	cd $(FRONTEND_DIR) && npm outdated

.PHONY: check-unused
check-unused:
	@echo "=== フロントエンドの未使用依存 ==="
	cd $(FRONTEND_DIR) && npx depcheck

.PHONY: audit
audit:
	@echo "=== フロントエンド依存の監査 ==="
	cd $(FRONTEND_DIR) && npm audit

.PHONY: update
update:
	@echo "=== フロントエンド依存の更新 ==="
	cd $(FRONTEND_DIR) && npm update

# 引数をそのまま渡すための設定
%:
	@:
