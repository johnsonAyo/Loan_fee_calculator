package main

import (
	"log/slog"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/api"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/infrastructure/repositories"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/infrastructure/strategies"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/services"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/telemetry"
)

func main() {
	telemetry.EmitEvent(slog.LevelInfo, "create_application_started", map[string]any{
		"app_name": "Loan Fee Calculation API",
	}, nil)

	// Dependency Injection
	repo := repositories.NewStaticFeeRepository()
	strategy := strategies.NewLinearInterpolationStrategy()
	service := services.NewFeeCalculatorService(repo, strategy)
	handler := api.NewAPIHandler(service)

	r := chi.NewRouter()

	// Middleware
	r.Use(middleware.RequestID)
	r.Use(middleware.RealIP)
	r.Use(middleware.Logger)
	r.Use(middleware.Recoverer)

	r.Use(cors.Handler(cors.Options{
		// AllowedOrigins: []string{"https://foo.com"}, // Use this to allow specific origin hosts
		AllowedOrigins:   []string{"*"}, // Follow Python CORS_ORIGINS
		AllowedMethods:   []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowedHeaders:   []string{"*"},
		AllowCredentials: true,
		MaxAge:           300, 
	}))

	r.Use(api.RateLimitMiddleware)

	// Routes
	r.Get("/", func(w http.ResponseWriter, r *http.Request) {
		telemetry.EmitEvent(slog.LevelInfo, "health_check_called", nil, nil)
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"status": "online", "service": "Loan Fee Calculator", "version": "1.0.0"}`))
	})

	r.Route("/api/v1", func(r chi.Router) {
		r.Post("/fees/calculate", handler.CalculateFee)
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8000"
	}

	telemetry.EmitEvent(slog.LevelInfo, "application_started", map[string]any{"port": port}, nil)
	if err := http.ListenAndServe(":"+port, r); err != nil {
		telemetry.EmitEvent(slog.LevelError, "server_crashed", nil, err)
		os.Exit(1)
	}
}
