import { LABEL } from "@/constants/fee-calculator"
import { ApiErrorResponse } from "@/types/fee-calculator"

export function getApiErrorMessage(payload: ApiErrorResponse | null): string {
  if (!payload) {
    return LABEL.genericError
  }
  if (typeof payload.detail === "string") {
    return payload.detail
  }
  if (Array.isArray(payload.detail) && payload.detail.length > 0) {
    const detail = payload.detail[0]
    const loc = Array.isArray(detail.loc) ? detail.loc.join(".") : "input"
    return `${loc}: ${detail.msg ?? "Invalid value"}`
  }
  if (payload.message) {
    return payload.message
  }
  if (payload.error) {
    return payload.error
  }
  return LABEL.fallbackError
}
