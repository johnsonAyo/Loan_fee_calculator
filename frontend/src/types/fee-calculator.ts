export type TermOption = "12" | "24"
export type SelectedTermOption = TermOption | ""

export type FeeRequest = {
  amount: string
  term: number
}

export type FeeResponse = {
  amount: string
  term: number
  fee: string
}

export type ApiValidationDetail = {
  loc?: Array<string | number>
  msg?: string
}

export type ApiErrorResponse = {
  message?: string
  error?: string
  detail?: ApiValidationDetail[] | string
}

export type CalculationSummaryItem = {
  label: string
  value: string
}


export type FeeCalculatorFormProps = {
  amount: string
  onAmountChange: (amount: string) => void
  term: SelectedTermOption
  onTermChange: (term: SelectedTermOption) => void
  amountValidationMessage: string
  isLoading: boolean
  canSubmit: boolean
}

export type FeeCalculatorFeedbackProps = {
  errorMessage: string
  result: FeeResponse | null
}

export type FeeCalculationApiResult =
  | { ok: true; data: FeeResponse }
  | { ok: false; status: number; error: ApiErrorResponse | null }
