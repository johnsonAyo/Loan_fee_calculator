import { CalculationSummaryItem, FeeResponse } from "@/types/fee-calculator"

export function toCurrency(value: string): string {
  const asNumber = Number(value)
  return new Intl.NumberFormat("en-GB", { style: "currency", currency: "GBP" }).format(asNumber)
}

export function toSummaryItems(result: FeeResponse): CalculationSummaryItem[] {
  return [
    { label: "Loan Amount", value: toCurrency(result.amount) },
    { label: "Term", value: `${result.term} months` },
    { label: "Fee", value: toCurrency(result.fee) },
    { label: "Total Payable", value: toCurrency(String(Number(result.amount) + Number(result.fee))) },
  ]
}
