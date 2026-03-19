import { FeeCalculator } from "@/components/fee-calculator"

export default function Home() {
  return (
    <div className="relative flex min-h-screen flex-1 flex-col items-center justify-center overflow-hidden bg-[#FAFAFA] px-4 py-12 sm:px-6 lg:px-8">
      {/* Ambient background glows */}
      <div className="pointer-events-none absolute top-[-10%] left-[-10%] h-[500px] w-[500px] rounded-full bg-blue-300/20 blur-[100px]" />
      <div className="pointer-events-none absolute bottom-[-10%] right-[-10%] h-[600px] w-[600px] rounded-full bg-indigo-300/20 blur-[120px]" />
      
      <main className="relative z-10 flex w-full max-w-4xl flex-col items-center gap-10">
        <header className="space-y-4 text-center max-w-2xl mx-auto">
          <div className="inline-flex items-center rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-sm font-semibold tracking-tight text-blue-800 shadow-sm mb-2">
            Welcome to the Loan Fee Calculator Web App
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 sm:text-4xl my-5">
            Calculate your loan fee instantly.
          </h1>
          <p className="text-lg text-slate-600 mt-2 font-medium">
            Discover your exact borrowing costs in seconds. No hidden fees, just straightforward transparent logic.
          </p>
        </header>
        <FeeCalculator />
      </main>
    </div>
  )
}
