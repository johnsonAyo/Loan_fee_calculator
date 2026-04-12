package api

import (
	"fmt"
	"log/slog"
	"net/http"
	"sync"

	"github.com/johnsonafuye/fee-calculator-backend-go/internal/telemetry"
	"golang.org/x/time/rate"
)

// Global map for IP rate limiters
var (
	visitors = make(map[string]*rate.Limiter)
	mu       sync.Mutex
)

func getLimiterForIP(ip string) *rate.Limiter {
	mu.Lock()
	defer mu.Unlock()
	limiter, exists := visitors[ip]
	if !exists {
		limiter = rate.NewLimiter(rate.Limit(5), 10)
		visitors[ip] = limiter
	}
	return limiter
}


func RateLimitMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip := r.RemoteAddr
		limiter := getLimiterForIP(ip)
		if !limiter.Allow() {
			telemetry.EmitEvent(slog.LevelWarn, "rate_limit_exceeded", map[string]any{
				"path": r.URL.Path,
			}, fmt.Errorf("rate limit exceeded"))
			
			http.Error(w, "Rate limit exceeded", http.StatusTooManyRequests)
			return
		}
		next.ServeHTTP(w, r)
	})
}
