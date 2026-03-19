.PHONY: install install-backend install-frontend dev dev-backend dev-frontend test test-backend test-frontend lint lint-backend lint-frontend build build-backend build-frontend test-e2e

install: install-backend install-frontend

install-backend:
	cd backend && python3 -m pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev:
	( cd backend && python3 -m uvicorn app.main:app --reload --port 8000 ) & \
	( cd frontend && npm run dev -- --port 3000 ) & \
	wait

dev-backend:
	cd backend && python3 -m uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev -- --port 3000

test: test-backend test-frontend

test-backend:
	cd backend && python3 -m pytest -q

test-frontend:
	cd frontend && npm run test:e2e

lint: lint-backend lint-frontend

lint-backend:
	cd backend && python3 -m ruff check app tests && python3 -m mypy app tests

lint-frontend:
	cd frontend && npm run lint

build: build-backend build-frontend

build-backend:
	cd backend && python3 -m compileall app tests

build-frontend:
	cd frontend && npm run build

test-e2e:
	cd frontend && npm run test:e2e
