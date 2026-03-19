import { TermOption } from "@/types/fee-calculator"

export const TERM_OPTIONS: Array<{ label: string; value: TermOption }> = [
  { label: "12 months", value: "12" },
  { label: "24 months", value: "24" },
]

export const LABEL = {
  title: "Loan Fee Calculator",
  description: "Get an instant, transparent quote in seconds.",
  amountLabel: "I want to borrow",
  amountHint: "Minimum £1,000 and maximum £20,000.",
  amountPlaceholder: "e.g  2000",
  termLabel: "Over",
  termPlaceholder: "Select loan term",
  submit: "Get your quote",
  submitLoading: "Calculating...",
  failedTitle: "Calculation Failed",
  completeTitle: "Calculation Complete",
  connectError: "Unable to connect to the API. Make sure the backend server is running.",
  genericError: "Unexpected error occurred while calculating the fee.",
  fallbackError: "Unable to process the request.",
}

export const MIN_BORROW_AMOUNT = 1000
export const MAX_BORROW_AMOUNT = 20000

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000"
