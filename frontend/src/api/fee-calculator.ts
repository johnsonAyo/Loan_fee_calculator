import { ApiErrorResponse, FeeCalculationApiResult, FeeRequest, FeeResponse } from "@/types/fee-calculator"
import { API_BASE_URL } from "@/constants/fee-calculator"
export async function calculateFee(payload: FeeRequest): Promise<FeeCalculationApiResult> {
  const response = await fetch(`${API_BASE_URL}/api/v1/fees/calculate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
  const json = (await response.json()) as ApiErrorResponse | FeeResponse

  if (!response.ok) {
    return { ok: false, status: response.status, error: json as ApiErrorResponse }
  }

  return { ok: true, data: json as FeeResponse }
}
