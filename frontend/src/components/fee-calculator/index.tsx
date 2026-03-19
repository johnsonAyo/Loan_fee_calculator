"use client"
import { CalculatorIcon } from "lucide-react"
import { LABEL } from "@/constants/fee-calculator"
import { useFeeCalculator } from "@/hooks/use-fee-calculator"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { FeeCalculatorFeedback } from "@/components/fee-calculator/feedback"
import { FeeCalculatorForm } from "@/components/fee-calculator/form"

export function FeeCalculator() {
  const {
    form,
    state,
    actions,
  } = useFeeCalculator()

  return (
    <div className="w-full max-w-xl">
      <Card className="w-full gap-2 rounded-3xl border border-white/40 bg-white/70 shadow-2xl shadow-blue-900/5 backdrop-blur-xl">
        <CardHeader className="space-y-3 pb-4">
          <CardTitle className="flex items-center gap-3 text-3xl font-bold tracking-tight text-slate-900">
            <span className="flex size-10 items-center justify-center rounded-xl bg-blue-600 text-white shadow-lg shadow-blue-600/20">
              <CalculatorIcon className="size-5" />
            </span>
            {LABEL.title}
          </CardTitle>
          <CardDescription className="text-lg font-medium tracking-tight text-slate-500">{LABEL.description}</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          <form className="space-y-5" onSubmit={actions.handleSubmit}>
            <FeeCalculatorForm
              amount={form.amount}
              onAmountChange={actions.setAmount}
              term={form.term}
              onTermChange={actions.setTerm}
              amountValidationMessage={form.amountValidationMessage}
              isLoading={state.isLoading}
              canSubmit={form.canSubmit}
            />
          </form>
          <FeeCalculatorFeedback errorMessage={state.errorMessage} result={state.result} />
        </CardContent>
      </Card>
    </div>
  )
}
