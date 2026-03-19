"use client"
import { FormEvent, useState } from "react"
import { calculateFee } from "@/api/fee-calculator"
import { LABEL } from "@/constants/fee-calculator"
import { getApiErrorMessage } from "@/lib/fee-calculator-error"
import { getAmountValidationMessage, getSubmitValidationError } from "@/lib/fee-calculator-validation"
import { FeeResponse, SelectedTermOption } from "@/types/fee-calculator"

export function useFeeCalculator() {
  const [amount, setAmount] = useState("")
  const [term, setTerm] = useState<SelectedTermOption>("")
  const [isLoading, setIsLoading] = useState(false)
  const [result, setResult] = useState<FeeResponse | null>(null)
  const [errorMessage, setErrorMessage] = useState("")
  const amountValidationMessage = getAmountValidationMessage(amount)
  const canSubmit = amount.trim().length > 0 && term !== "" && amountValidationMessage === "" && !isLoading

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setResult(null)
    setErrorMessage("")
    setIsLoading(true)
    try {
      const formData = new FormData(event.currentTarget)
      const submittedAmount = String(formData.get("loan-amount") ?? "").trim()
      const submitValidationError = getSubmitValidationError({
        submittedAmount,
        amountValidationMessage,
        term,
      })
      if (submitValidationError) {
        setErrorMessage(submitValidationError)
        return
      }
      const apiResult = await calculateFee({ amount: submittedAmount, term: Number(term) })
      if (!apiResult.ok) {
        setErrorMessage(getApiErrorMessage(apiResult.error))
        return
      }
      setResult(apiResult.data)
    } catch {
      setErrorMessage(LABEL.connectError)
    } finally {
      setIsLoading(false)
    }
  }

  return {
    form: {
      amount,
      term,
      amountValidationMessage,
      canSubmit,
    },
    state: {
      isLoading,
      result,
      errorMessage,
    },
    actions: {
      setAmount,
      setTerm,
      handleSubmit,
    },
  }
}
