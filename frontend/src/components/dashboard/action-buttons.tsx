import React from 'react';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-react';

export const ActionButtons = () => {
  return (
    <div className="flex items-center gap-4 mb-6">
      <Button>
        <PlusCircle className="h-4 w-4 mr-2" />
        Registrar Ingreso
      </Button>
      <Button variant="secondary">
        <PlusCircle className="h-4 w-4 mr-2" />
        Registrar Gasto
      </Button>
    </div>
  );
};
