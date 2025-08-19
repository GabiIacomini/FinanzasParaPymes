"use client";

import React, { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowDownRight, ArrowUpRight } from 'lucide-react';

// Define a type for our currency data
type Currency = {
  nombre: string;
  compra: number;
  venta: number;
};

// Mock data that mimics the API response
const mockData: Currency[] = [
    { nombre: 'Dólar Oficial', compra: 1270.00, venta: 1310.00 },
    { nombre: 'Dólar Blue', compra: 1320.00, venta: 1340.00 },
    { nombre: 'Euro', compra: 1493.73, venta: 1507.44 },
    { nombre: 'Real', compra: 234.55, venta: 234.68 },
];


export const CurrencyBanner = () => {
  const [data, setData] = useState<Currency[]>(mockData);
  const [loading, setLoading] = useState(false); // Set to false since we are using mock data
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // NOTE: API fetching logic will be implemented here.
    // For now, we are using mock data to build the UI.
    /*
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      try {
        const urls = [
          'https://dolarapi.com/v1/dolares/oficial',
          'https://dolarapi.com/v1/dolares/blue',
          'https://dolarapi.com/v1/cotizaciones/eur',
          'https://dolarapi.com/v1/cotizaciones/brl',
        ];
        const responses = await Promise.all(urls.map(url => fetch(url)));
        const jsonData = await Promise.all(responses.map(res => res.json()));

        const formattedData = jsonData.map(item => ({
            nombre: item.nombre,
            compra: item.compra,
            venta: item.venta,
        }));

        setData(formattedData);
      } catch (e) {
        setError('Failed to fetch currency data.');
        console.error(e);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    */
  }, []);

  if (loading) {
    return <div className="text-center p-4">Cargando cotizaciones...</div>;
  }

  if (error) {
    return <div className="text-center p-4 text-red-500">{error}</div>;
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {data.map((currency) => (
        <Card key={currency.nombre}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">{currency.nombre}</CardTitle>
            {/* Placeholder icon */}
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" className="h-4 w-4 text-muted-foreground"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
                <div className="text-xs text-muted-foreground">Compra</div>
                <div className="text-lg font-bold">${currency.compra.toFixed(2)}</div>
            </div>
            <div className="flex items-center justify-between">
                <div className="text-xs text-muted-foreground">Venta</div>
                <div className="text-lg font-bold">${currency.venta.toFixed(2)}</div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
};
