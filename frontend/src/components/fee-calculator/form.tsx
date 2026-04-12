"use client"
import { Loader2Icon } from "lucide-react"
import { LABEL, TERM_OPTIONS } from "@/constants/fee-calculator"    
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { FeeCalculatorFormProps } from "@/types/fee-calculator"

export function FeeCalculatorForm(props: FeeCalculatorFormProps) {
  const { amount, onAmountChange, term, onTermChange, amountValidationMessage, isLoading, canSubmit } = props
  return (
    <div className="space-y-8">
      <div className="space-y-6 rounded-2xl border border-slate-100 bg-slate-50/50 p-6 shadow-sm">
        <div className="space-y-3">
          <Label htmlFor="loan-amount" className="text-sm font-bold tracking-tight text-slate-700">
            {LABEL.amountLabel}
          </Label>
          <div className="relative">
            <span className="pointer-events-none absolute top-1/2 left-4 -translate-y-1/2 text-lg font-medium text-slate-400">£</span>
            <Input
              id="loan-amount"
              name="loan-amount"
              inputMode="decimal"
              placeholder={LABEL.amountPlaceholder}
              value={amount}
              data-testid="amount-input"
              onChange={(event) => onAmountChange(event.target.value)}
              className="h-14 rounded-xl border-slate-200 bg-white pl-8 text-lg font-medium text-slate-900 shadow-sm transition-all focus-visible:border-blue-600 focus-visible:ring-4 focus-visible:ring-blue-600/10"
              required
            />
          </div>
          {amountValidationMessage ? (
            <p className="text-sm font-semibold text-red-600">{amountValidationMessage}</p>
          ) : null}
        </div>

        <div className="space-y-3">
          <Label className="text-sm font-bold tracking-tight text-slate-700">{LABEL.termLabel}</Label>
          <div className="grid grid-cols-2 gap-3">
            {TERM_OPTIONS.map((option) => (
              <button
                key={option.value}
                data-testid={`term-option-${option.value}`}
                aria-pressed={term === option.value}
                type="button"
                onClick={() => onTermChange(option.value)}
                className={`flex h-14 items-center justify-center rounded-xl border-2 text-lg font-bold transition-all ${
                  term === option.value
                    ? "border-blue-600 bg-blue-50/50 text-blue-700 shadow-sm"
                    : "border-slate-200 bg-white text-slate-500 hover:border-slate-300 hover:bg-slate-50"
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      <p className="text-sm text-center font-medium text-slate-500">{LABEL.amountHint}</p>

      <Button
        type="submit"
        data-testid="submit-quote"
        className="h-14 w-full rounded-xl bg-blue-600 text-lg font-bold text-white shadow-lg shadow-blue-600/20 transition-all hover:bg-blue-700 hover:shadow-blue-600/30 active:scale-[0.98]"
        disabled={!canSubmit}
      >
        {isLoading ? <Loader2Icon className="mr-2 size-5 animate-spin" /> : null}
        {isLoading ? LABEL.submitLoading : LABEL.submit}
      </Button>
    </div>
  )
}
