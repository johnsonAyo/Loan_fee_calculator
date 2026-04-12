import { MAX_BORROW_AMOUNT, MIN_BORROW_AMOUNT } from "@/constants/fee-calculator"
import { SelectedTermOption } from "@/types/fee-calculator"

export function sanitizeAmountInput(rawValue: string): string {
  return rawValue
    .replace(/[^0-9.]/g, "")
    .replace(/(\..*?)\./g, "$1")
}


export function getAmountValidationMessage(amount: string): string {
  const trimmed = amount.trim()
  if (!trimmed) {
    return ""
  }
  const decimalPointCount = (trimmed.match(/\./g) ?? []).length
  if (decimalPointCount > 1) {
    return "Amount must have at most 2 decimal places."
  }
  const decimalPart = trimmed.split(".")[1]
  if (decimalPart && decimalPart.length > 2) {
    return "Amount must have at most 2 decimal places."
  }
  const parsed = Number(trimmed)
  if (Number.isNaN(parsed)) {
    return "Enter a valid amount."
  }
  if (parsed < MIN_BORROW_AMOUNT) {
    return `Amount must be at least £${MIN_BORROW_AMOUNT.toLocaleString("en-GB")}.`
  }
  if (parsed > MAX_BORROW_AMOUNT) {
    return `Amount must not be more than £${MAX_BORROW_AMOUNT.toLocaleString("en-GB")}.`
  }
  return ""
}

type SubmitValidationInput = {
  submittedAmount: string
  amountValidationMessage: string
  term: SelectedTermOption
}

export function getSubmitValidationError(input: SubmitValidationInput): string {
  const { submittedAmount, amountValidationMessage, term } = input
  if (!submittedAmount) {
    return "loan-amount: Invalid value"
  }
  if (amountValidationMessage) {
    return amountValidationMessage
  }
  if (term === "") {
    return "term: Invalid value"
  }
  return ""
}
