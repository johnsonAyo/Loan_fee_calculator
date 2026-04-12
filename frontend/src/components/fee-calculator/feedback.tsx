import { AlertCircleIcon, CheckCircle2Icon } from "lucide-react"
import { LABEL,toTestIdToken } from "@/constants/fee-calculator"
import { toSummaryItems } from "@/lib/fee-calculator-format"
import { FeeCalculatorFeedbackProps } from "@/types/fee-calculator"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
export function FeeCalculatorFeedback(props: FeeCalculatorFeedbackProps) {
  const { errorMessage, result } = props
  return (
    <>
      {errorMessage ? (
        <Alert variant="destructive" className="rounded-xl">
          <AlertCircleIcon className="size-5" />
          <AlertTitle className="font-semibold text-base mb-2">{LABEL.failedTitle}</AlertTitle>
          <AlertDescription className="text-sm font-medium">{errorMessage}</AlertDescription>
        </Alert>
      ) : null}

      {result ? (
        <div
          data-testid="result-panel"
          className="overflow-hidden rounded-2xl border border-emerald-100 bg-emerald-50 px-6 py-5 shadow-sm"
        >
          <div className="flex items-center gap-3 border-b border-emerald-100 pb-4">
            <div className="flex size-8 shrink-0 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
              <CheckCircle2Icon className="size-5" />
            </div>
            <h3 data-testid="result-title" className="m-0 text-xl font-bold tracking-tight text-emerald-950">
              {LABEL.completeTitle}
            </h3>
          </div>
          <div className="mt-4 space-y-3 pt-2">
            {toSummaryItems(result).map((item) => (
              <div key={item.label} className="flex items-center justify-between text-base">
                <span
                  data-testid={`result-label-${toTestIdToken(item.label)}`}
                  className="font-medium text-emerald-900/70"
                >
                  {item.label}
                </span>
                <span
                  data-testid={`result-value-${toTestIdToken(item.label)}`}
                  className="font-bold text-emerald-950"
                >
                  {item.value}
                </span>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </>
  )
}
