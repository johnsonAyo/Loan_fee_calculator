.PHONY: install install-backend install-backend-go install-backend-dotnet install-frontend dev dev-backend dev-backend-go dev-backend-dotnet dev-frontend test test-backend test-backend-go test-backend-dotnet test-frontend lint lint-backend lint-frontend build build-backend build-backend-go build-backend-dotnet build-frontend test-e2e
install: install-backend install-frontend

install-backend:
	cd backend && python3 -m pip install -r requirements.txt

install-backend-go:
	cd backend-go && go mod tidy

install-backend-dotnet:
	cd backend-dotnet && ~/.dotnet/dotnet restore

install-frontend:
	cd frontend && npm install

dev:
	( cd backend && python3 -m uvicorn app.main:app --reload --port 8000 ) & \
	( cd frontend && npm run dev -- --port 3000 ) & \
	wait

dev-backend:
	cd backend && python3 -m uvicorn app.main:app --reload --port 8000

dev-backend-go:
	cd backend-go && PORT=8000 go run cmd/api/main.go

dev-backend-dotnet:
	cd backend-dotnet/LoanFeeCalculator.Api && ~/.dotnet/dotnet run --urls="http://127.0.0.1:8000"

dev-frontend:
	cd frontend && npm run dev -- --port 3000

test: test-backend test-frontend

test-backend:
	cd backend && python3 -m pytest -q

test-backend-go:
	cd backend-go && go test ./...

test-backend-dotnet:
	cd backend-dotnet && ~/.dotnet/dotnet test

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

build-backend-go:
	cd backend-go && go build -o bin/api cmd/api/main.go

build-backend-dotnet:
	cd backend-dotnet/LoanFeeCalculator.Api && ~/.dotnet/dotnet publish -c Release -o ../bin

build-frontend:
	cd frontend && npm run build

test-e2e:
	cd frontend && npm run test:e2e
