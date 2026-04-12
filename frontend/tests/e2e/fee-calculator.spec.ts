import { expect, test } from "@playwright/test"

test("renders fee calculator shell", async ({ page }) => {
  await page.goto("/")
  await expect(page.getByRole("heading").first()).toBeVisible()
  await expect(page.getByTestId("amount-input")).toBeVisible()
  await expect(page.getByTestId("term-option-12")).toBeVisible()
  await expect(page.getByTestId("term-option-24")).toBeVisible()
  await expect(page.getByTestId("submit-quote")).toBeVisible()
})

test("accepts input, selects term, submits quote, and asserts result values", async ({ page }) => {
  await page.route("**/fees/calculate", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        amount: "1500",
        term: 24,
        fee: "105",
      }),
    })
  })

  await page.goto("/")
  await page.getByTestId("amount-input").fill("900")
  await expect(page.getByTestId("amount-input")).toHaveValue("900")
  await expect(page.getByTestId("submit-quote")).toBeDisabled()
  await page.getByTestId("amount-input").fill("30000")
  await expect(page.getByTestId("submit-quote")).toBeDisabled()
  await page.getByTestId("amount-input").fill("1500")
  await page.getByTestId("term-option-24").click()
  await expect(page.getByTestId("term-option-24")).toHaveAttribute("aria-pressed", "true")
  await expect(page.getByTestId("submit-quote")).toBeEnabled()

  await page.getByTestId("submit-quote").click()
  await expect(page.getByTestId("result-panel")).toBeVisible()
  await expect(page.getByTestId("result-title")).toBeVisible()
  await expect(page.getByTestId("result-label-loan-amount")).toHaveText("Loan Amount")
  await expect(page.getByTestId("result-value-loan-amount")).toHaveText("£1,500.00")
  await expect(page.getByTestId("result-label-term")).toHaveText("Term")
  await expect(page.getByTestId("result-value-term")).toHaveText("24 months")
  await expect(page.getByTestId("result-label-fee")).toHaveText("Fee")
  await expect(page.getByTestId("result-value-fee")).toHaveText("£105.00")
  await expect(page.getByTestId("result-label-total-payable")).toHaveText("Total Payable")
  await expect(page.getByTestId("result-value-total-payable")).toHaveText("£1,605.00")
})
