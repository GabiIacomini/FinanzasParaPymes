import React from 'react';
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { ArrowUpCircle, ArrowDownCircle } from 'lucide-react';

const mockTransactions = [
  {
    id: '1',
    type: 'income',
    description: 'Venta de servicios de consultoría',
    amount: 250000,
    date: '2025-08-18T10:30:00Z',
    category: 'Ventas',
  },
  {
    id: '2',
    type: 'expense',
    description: 'Alquiler de oficina',
    amount: -150000,
    date: '2025-08-17T14:00:00Z',
    category: 'Alquiler',
  },
  {
    id: '3',
    type: 'expense',
    description: 'Compra de insumos',
    amount: -45000,
    date: '2025-08-16T11:20:00Z',
    category: 'Insumos',
  },
  {
    id: '4',
    type: 'income',
    description: 'Factura #1254',
    amount: 120000,
    date: '2025-08-15T18:45:00Z',
    category: 'Ventas',
  },
];

const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value);
};

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('es-AR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    });
}

export const RecentTransactions = () => {
  return (
    <div className="mt-6">
      <h3 className="text-xl font-bold mb-4">Transacciones Recientes</h3>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[200px]">Descripción</TableHead>
            <TableHead>Categoría</TableHead>
            <TableHead>Fecha</TableHead>
            <TableHead className="text-right">Monto</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {mockTransactions.map((transaction) => (
            <TableRow key={transaction.id}>
              <TableCell className="font-medium flex items-center">
                {transaction.type === 'income' ?
                    <ArrowUpCircle className="h-4 w-4 mr-2 text-green-500" /> :
                    <ArrowDownCircle className="h-4 w-4 mr-2 text-red-500" />}
                {transaction.description}
              </TableCell>
              <TableCell>
                <Badge variant="outline">{transaction.category}</Badge>
              </TableCell>
              <TableCell>{formatDate(transaction.date)}</TableCell>
              <TableCell className={`text-right font-bold ${transaction.type === 'income' ? 'text-green-600' : 'text-red-600'}`}>
                {formatCurrency(transaction.amount)}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};
