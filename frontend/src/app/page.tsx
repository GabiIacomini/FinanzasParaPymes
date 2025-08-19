import { WelcomeMessage } from "@/components/dashboard/welcome-message";
import { CurrencyBanner } from "@/components/dashboard/currency-banner";
import { SummaryCards } from "@/components/dashboard/summary-cards";
import { ActionButtons } from "@/components/dashboard/action-buttons";
import { TransactionsChart } from "@/components/dashboard/transactions-chart";
import { RecentTransactions } from "@/components/dashboard/recent-transactions";
import { TransactionModal } from "@/components/dashboard/transaction-modal";

export default function HomePage() {
  return (
    <div className="container mx-auto py-8 px-4">
      <WelcomeMessage />
      <CurrencyBanner />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
        <div className="md:col-span-2">
          <ActionButtons />
          <SummaryCards />
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 my-6">
        <TransactionsChart />
        {/* Placeholder for Expense Categories */}
      </div>

      <RecentTransactions />

      {/* The modal is included here but will be controlled by state */}
      <TransactionModal />
    </div>
  );
}
