import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { DollarSign, TrendingUp, TrendingDown, ArrowLeftRight } from 'lucide-react';

const mockSummaryData = {
  income: 1250000.75,
  expenses: 785450.50,
  balance: 464550.25,
  transactions: 124,
};

export const SummaryCards = () => {
  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value);
  };

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Ingresos del Mes</CardTitle>
          <TrendingUp className="h-4 w-4 text-muted-foreground text-green-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{formatCurrency(mockSummaryData.income)}</div>
          <p className="text-xs text-muted-foreground">+15.2% desde el mes pasado</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Egresos del Mes</CardTitle>
          <TrendingDown className="h-4 w-4 text-muted-foreground text-red-500" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{formatCurrency(mockSummaryData.expenses)}</div>
          <p className="text-xs text-muted-foreground">+8.1% desde el mes pasado</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Balance Neto</CardTitle>
          <DollarSign className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{formatCurrency(mockSummaryData.balance)}</div>
           <p className="text-xs text-muted-foreground">Balance actual del mes</p>
        </CardContent>
      </Card>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Transacciones</CardTitle>
          <ArrowLeftRight className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">+{mockSummaryData.transactions}</div>
          <p className="text-xs text-muted-foreground">En el último mes</p>
        </CardContent>
      </Card>
    </div>
  );
};
