import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground">
      <div className="container flex flex-col items-center justify-center gap-12 px-4 py-16 ">
        <div className="flex flex-col items-center gap-2 text-center">
          <h1 className="text-5xl font-extrabold tracking-tight">
            Plataforma de Análisis Financiero
          </h1>
          <p className="text-2xl text-muted-foreground">
            Proyecciones para Pymes en el contexto argentino.
          </p>
        </div>
        <div className="flex gap-4">
          <Button>Empezar</Button>
          <Button variant="secondary">Ver Demo</Button>
          <Button variant="outline">Contacto</Button>
        </div>
      </div>
    </main>
  );
}
