package telemetry

import (
	"log/slog"
	"os"
)

var Logger *slog.Logger

func init() {
	handler := slog.NewJSONHandler(os.Stdout, nil)
	Logger = slog.New(handler)
}

func EmitEvent(level slog.Level, eventName string, attrs map[string]any, err error) {
	args := []any{
		slog.String("event", eventName),
	}
	for k, v := range attrs {
		args = append(args, slog.Any(k, v))
	}
	if err != nil {
		args = append(args, slog.Any("error", err.Error()))
	}
	
	// context.Background() is omitted for simple logging here globally
	if level == slog.LevelError {
		Logger.Error(eventName, args...)
	} else if level == slog.LevelWarn {
		Logger.Warn(eventName, args...)
	} else {
		Logger.Info(eventName, args...)
	}
}
