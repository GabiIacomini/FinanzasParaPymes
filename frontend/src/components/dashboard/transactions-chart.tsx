"use client";

import React from 'react';
import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

const mockChartData = [
  { name: 'Lun', total: Math.floor(Math.random() * 50000) + 10000 },
  { name: 'Mar', total: Math.floor(Math.random() * 50000) + 10000 },
  { name: 'Mié', total: Math.floor(Math.random() * 50000) + 10000 },
  { name: 'Jue', total: Math.floor(Math.random() * 50000) + 10000 },
  { name: 'Vie', total: Math.floor(Math.random() * 50000) + 10000 },
  { name: 'Sáb', total: Math.floor(Math.random() * 50000) + 10000 },
  { name: 'Dom', total: Math.floor(Math.random() * 50000) + 10000 },
];

export const TransactionsChart = () => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Resumen Semanal</CardTitle>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={mockChartData}>
            <XAxis
              dataKey="name"
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `$${value / 1000}k`}
            />
            <Tooltip
                cursor={{fill: 'transparent'}}
                contentStyle={{background: 'hsl(var(--background))', border: '1px solid hsl(var(--border))', borderRadius: 'var(--radius)'}}
            />
            <Legend />
            <Bar dataKey="total" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} name="Transacciones" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
};
