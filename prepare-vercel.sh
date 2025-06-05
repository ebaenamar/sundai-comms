#!/bin/bash

# Crear una rama específica para Vercel
git checkout -b vercel-deploy

# Copiar archivos de frontend a la raíz
cp -r frontend/src ./
cp -r frontend/public ./
cp frontend/package.json ./package.json
cp frontend/package-lock.json ./package-lock.json
cp frontend/next.config.js ./next.config.js
cp frontend/postcss.config.js ./postcss.config.js
cp frontend/tailwind.config.js ./tailwind.config.js
cp frontend/tsconfig.json ./tsconfig.json
cp frontend/next-env.d.ts ./next-env.d.ts

# Eliminar vercel.json en la raíz (usaremos el de frontend)
rm -f vercel.json
cp frontend/vercel.json ./vercel.json

# Commit de los cambios
git add .
git commit -m "chore: prepare for vercel deployment"

# Push de la rama a GitHub
git push -u origin vercel-deploy

echo "Rama vercel-deploy creada y subida a GitHub. Ahora puedes desplegar esta rama en Vercel."
