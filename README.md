# Loan Fee Calculation Monorepo

This repository is split into two workspaces:

- `backend/` FastAPI fee calculation API and Python tests
- `frontend/` Next.js + shadcn/ui application and Playwright tests

## Orchestrator Commands

Run from repository root:

```bash
make install
make dev
```

`make dev` starts backend on `http://127.0.0.1:8000` and frontend on `http://127.0.0.1:3000`.

## Additional Commands

```bash
make dev-backend
make dev-frontend
make test
make lint
make build
make test-e2e
```
