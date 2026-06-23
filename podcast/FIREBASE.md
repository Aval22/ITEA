# Valoraciones por estrellas (Firebase) — puesta en marcha

Las páginas del podcast tienen valoración por estrellas (máx. 5) con **media y nº de
votos compartido entre todos los visitantes**. Eso necesita una pequeña base de datos:
usamos **Firebase Firestore** (gratis para este volumen).

Mientras la config esté vacía, las estrellas funcionan en **modo local** (cada visitante
ve solo su voto en su navegador). Al pegar la config, pasan a **modo compartido**.

## 1. Crear el proyecto (una vez, ~5 min)

1. Entra en **https://console.firebase.google.com** e inicia sesión con tu cuenta Google.
2. **Add project** → nombre p. ej. `itea-podcast` → puedes desactivar Google Analytics → **Create**.
3. Menú izquierdo **Build → Firestore Database** → **Create database** →
   modo **Production** → elige región (p. ej. `eur3 (europe-west)`) → **Enable**.

## 2. Registrar la app web y copiar la config

1. En **Project settings** (rueda dentada, arriba) → pestaña **General** →
   baja a **Your apps** → icono **</>** (Web).
2. Apodo: `itea-podcast-web` → **Register app** (no hace falta Hosting).
3. Verás un objeto `firebaseConfig = { apiKey:"…", projectId:"…", … }`. **Cópialo.**
4. Pega esos valores en **los dos archivos**, `podcast.html` y `podcast_en.html`,
   dentro del bloque `const firebaseConfig = { … }` (arriba del `<script type="module">`).
   > Usa el **mismo** proyecto en ambos para que los votos se sumen entre ES y EN.
   > La `apiKey` web es pública por diseño; no es un secreto.

## 3. Reglas de seguridad de Firestore

En **Firestore Database → Rules**, pega esto y pulsa **Publish**. Permite leer a todos y
votar de forma controlada (solo la colección `ratings`, sumando 1 voto y 1–5 estrellas):

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /ratings/{epId} {
      allow read: if true;

      // crear el primer voto del episodio
      allow create: if request.resource.data.count == 1
                    && request.resource.data.sum is int
                    && request.resource.data.sum >= 1
                    && request.resource.data.sum <= 5;

      // sumar un voto (count +1, sum sube entre 1 y 5)
      allow update: if request.resource.data.count == resource.data.count + 1
                    && request.resource.data.sum >= resource.data.sum + 1
                    && request.resource.data.sum <= resource.data.sum + 5;

      allow delete: if false;
    }
    match /{document=**} { allow read, write: if false; }
  }
}
```

## 4. Subir los cambios

```zsh
cd "/Users/agll/Documents/Claude/Projects/Framework ITEA"
git add podcast.html podcast_en.html podcast/FIREBASE.md
git commit -m "Podcast: ratings (Firebase) + share + contact"
git push
```

Listo. Cada visitante puede votar una vez por episodio (se recuerda en su navegador) y la
media + nº de votos se actualizan para todos.

## Notas
- **Límite de voto**: el bloqueo de "un voto por persona" es por navegador (localStorage).
  Es suficiente para una web divulgativa; no es un sistema antifraude estricto.
- **Coste**: el plan gratuito (Spark) cubre de sobra este tráfico. No hace falta tarjeta.
- **Reset**: para reiniciar un contador, borra el documento del episodio en Firestore
  (colección `ratings`, doc `ep1`…`ep8`).
