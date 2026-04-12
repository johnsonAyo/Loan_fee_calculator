package api

import (
	"encoding/json"
	"log/slog"
	"net/http"

	"github.com/johnsonafuye/fee-calculator-backend-go/internal/domain"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/services"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/telemetry"
	"github.com/shopspring/decimal"
)

type LoanRequest struct {
	Amount decimal.Decimal `json:"amount"`
	Term   int             `json:"term"`
}

type FeeResponse struct {
	Amount string `json:"amount"`
	Term   int    `json:"term"`
	Fee    string `json:"fee"`
}

type ErrorResponse struct {
	Code    string `json:"code"`
	Message string `json:"message"`
}

type APIHandler struct {
	service *services.FeeCalculatorService
}

func NewAPIHandler(service *services.FeeCalculatorService) *APIHandler {
	return &APIHandler{service: service}
}

func (h *APIHandler) CalculateFee(w http.ResponseWriter, r *http.Request) {
	var payload LoanRequest
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		h.writeError(w, http.StatusUnprocessableEntity, "VALIDATION_ERROR", "Invalid JSON payload")
		return
	}

	app, err := domain.NewLoanApplication(payload.Amount, payload.Term)
	if err != nil {
		h.handleDomainError(w, r, payload.Amount, payload.Term, err)
		return
	}

	fee, err := h.service.CalculateFee(app)
	if err != nil {
		h.handleDomainError(w, r, payload.Amount, payload.Term, err)
		return
	}

	telemetry.EmitEvent(slog.LevelInfo, "calculate_fee_completed", map[string]any{
		"amount": payload.Amount.String(),
		"term":   payload.Term,
		"fee":    fee.String(),
	}, nil)

	response := FeeResponse{
		Amount: payload.Amount.String(),
		Term:   payload.Term,
		Fee:    fee.String(),
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}

func (h *APIHandler) handleDomainError(w http.ResponseWriter, r *http.Request, amount decimal.Decimal, term int, err error) {
	telemetry.EmitEvent(slog.LevelError, "domain_exception_handler_triggered", map[string]any{
		"path":   r.URL.Path,
		"amount": amount.String(),
		"term":   term,
	}, err)

	switch e := err.(type) {
	case *domain.LoanValidationError:
		h.writeError(w, http.StatusUnprocessableEntity, "VALIDATION_ERROR", e.Message)
	case *domain.BreakpointNotFoundError:
		h.writeError(w, http.StatusUnprocessableEntity, "VALIDATION_ERROR", e.Message)
	case *domain.CalculationError:
		h.writeError(w, http.StatusUnprocessableEntity, "VALIDATION_ERROR", e.Message)
	default:
		h.writeError(w, http.StatusInternalServerError, "INTERNAL_ERROR", "An unexpected error occurred")
	}
}

func (h *APIHandler) writeError(w http.ResponseWriter, status int, code, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(ErrorResponse{
		Code:    code,
		Message: message,
	})
}
