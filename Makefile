.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Express API (Backend)
api-build: ## Build Express Api
	npm --prefix ./velov-waiting-time-api/ run build

api-start: ## Start Express Api
	npm --prefix ./velov-waiting-time-api/ run start

api-dev: ## Start Express Api in dev mode
	npm --prefix ./velov-waiting-time-api/ run start:nodemon

# React App (Frontend)
app-build: ## Build React App
	npm --prefix ./velov-waiting-time-app/ run build

app-start: ## Start React App
	npm --prefix ./velov-waiting-time-app/ run start
