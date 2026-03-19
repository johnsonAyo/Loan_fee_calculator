import { expect, test } from "@playwright/test"

test("renders fee calculator shell", async ({ page }) => {
  await page.goto("/")
  await expect(page.getByRole("heading").first()).toBeVisible()
  await expect(page.locator("#loan-amount")).toBeVisible()
  await expect(page.getByRole("button", { name: "Get your quote" })).toBeVisible()
})

test("accepts amount typing and keeps submit available", async ({ page }) => {
  await page.goto("/")
  await page.locator("#loan-amount").fill("900")
  await expect(page.locator("#loan-amount")).toHaveValue("900")
  await expect(page.getByText("Amount must be at least £1,000.")).toBeVisible()
  await expect(page.getByRole("button", { name: "Get your quote" })).toBeDisabled()
  await page.locator("#loan-amount").fill("30000")
  await expect(page.getByText("Amount must be no more than £20,000.")).toBeVisible()
  await expect(page.getByRole("button", { name: "Get your quote" })).toBeDisabled()
  await page.locator("#loan-amount").fill("1500")
  await page.getByRole("button", { name: "24 months" }).click()
  await expect(page.getByRole("button", { name: "Get your quote" })).toBeEnabled()
})
