# Etapa 1: Builder - Compila la aplicación
FROM node:20-alpine AS builder
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código fuente
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: Runner - Ejecuta la aplicación
FROM node:20-alpine AS runner
WORKDIR /app

# Crear un usuario no-root para mayor seguridad
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copiar la salida 'standalone' del builder
COPY --from=builder /app/.next/standalone ./

# Copiar los assets públicos y estáticos
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/static ./.next/static

# Cambiar al usuario no-root
USER nextjs

# Exponer el puerto
EXPOSE 3000

# Comando para iniciar el servidor
CMD ["node", "server.js"]
