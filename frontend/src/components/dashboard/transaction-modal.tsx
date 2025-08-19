"use client"

import React, { useState } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
// NOTE: A proper DatePicker would require Popover and Calendar, which is a bit complex
// for this step. Using a simple Input type="date" for now.
// I will create the full DatePicker if we refine this component later.


const incomeCategories = [
    { value: 'ventas', label: 'Ventas' },
    { value: 'consultoria', label: 'Consultoría' },
    { value: 'otros', label: 'Otros Ingresos' },
];

const expenseCategories = [
    { value: 'alquiler', label: 'Alquiler' },
    { value: 'insumos', label: 'Insumos' },
    { value: 'salarios', label: 'Salarios' },
    { value: 'servicios', label: 'Servicios Públicos' },
    { value: 'marketing', label: 'Marketing' },
    { value: 'otros', label: 'Otros Gastos' },
];

// This is a placeholder for the real modal which would be controlled by state from its parent
export const TransactionModal = () => {
    const [type, setType] = useState('expense');

    const categories = type === 'income' ? incomeCategories : expenseCategories;
    const quickAmounts = [1000, 5000, 10000, 25000, 50000];

  return (
    // In a real app, the `open` prop would be controlled by state
    <Dialog open={false}>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Registrar Transacción</DialogTitle>
          <DialogDescription>
            Añade un nuevo ingreso o gasto a tus registros.
          </DialogDescription>
        </DialogHeader>
        <Tabs defaultValue="expense" onValueChange={setType} className="w-full">
            <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="income">Ingreso</TabsTrigger>
                <TabsTrigger value="expense">Gasto</TabsTrigger>
            </TabsList>
            <TabsContent value="income">
                {/* Income Form would be here */}
            </TabsContent>
            <TabsContent value="expense">
                {/* Expense Form would be here */}
            </TabsContent>
        </Tabs>
        <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="amount" className="text-right">Monto</Label>
                <Input id="amount" type="number" placeholder="ARS 0.00" className="col-span-3" />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label className="text-right">Rápido</Label>
                <div className="col-span-3 flex gap-2">
                    {quickAmounts.map(amount => (
                        <Button key={amount} variant="outline" size="sm" className="flex-1">
                            ${amount/1000}k
                        </Button>
                    ))}
                </div>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="date" className="text-right">Fecha</Label>
                <Input id="date" type="date" className="col-span-3" />
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="category" className="text-right">Categoría</Label>
                <Select>
                    <SelectTrigger className="col-span-3">
                        <SelectValue placeholder={`Seleccionar categoría de ${type === 'income' ? 'ingreso' : 'gasto'}`} />
                    </SelectTrigger>
                    <SelectContent>
                        {categories.map(cat => (
                            <SelectItem key={cat.value} value={cat.value}>{cat.label}</SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            </div>
            <div className="grid grid-cols-4 items-center gap-4">
                <Label htmlFor="description" className="text-right">Descripción</Label>
                <Textarea id="description" placeholder="Escribe una descripción..." className="col-span-3" />
            </div>
        </div>
        <DialogFooter>
          <DialogClose asChild>
            <Button variant="ghost">Cancelar</Button>
          </DialogClose>
          <Button type="submit">Registrar Transacción</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};
