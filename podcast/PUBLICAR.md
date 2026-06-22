# Publicar el ITEA Podcast

Los audios **no** se versionan en el repo (engordarían el historial). Se sirven como
**assets de un GitHub Release** y las páginas los enlazan por URL.

## 1. Crear el Release con los audios (una sola vez)

Los 8 MP3 ya están renombrados y listos en `podcast/release-assets/`
(formato `es-<archivo>.mp3`). Sube ese mismo nombre como asset.

Opción web: GitHub → repo `Aval22/ITEA` → **Releases** → **Draft a new release**
- **Tag**: `podcast-v1`  (debe coincidir con el del HTML)
- Arrastra los 8 archivos de `podcast/release-assets/`
- **Publish release**

Opción CLI (con `gh`):
```bash
cd podcast/release-assets
gh release create podcast-v1 *.mp3 -t "ITEA Podcast — audios" -n "Episodios en español"
```

## 2. Subir las páginas (NO los audios)

```bash
git add podcast.html podcast_en.html podcast/itea-podcast-logo.svg podcast/PUBLICAR.md \
        index.html index_en.html .gitignore
git commit -m "Add ITEA Podcast page (audio via Release podcast-v1)"
git push
```
> `*.mp3` y `podcast/release-assets/` están en `.gitignore`: los audios no se subirán al repo.

URL final: https://aval22.github.io/ITEA/podcast.html

## 3. Añadir otro idioma a un episodio

1. Sube el MP3 al mismo Release con el nombre `<idioma>-<archivo>.mp3`
   (p. ej. `en-ep1-grados-prueba-ia-agentica.mp3`).
2. En `podcast.html` / `podcast_en.html`, dentro del array `EP`, cambia ese idioma
   de `null` al nombre base. Ejemplo:
   ```js
   audio:{es:"ep1-grados-prueba-ia-agentica", en:"ep1-grados-prueba-ia-agentica", pt:null, zh:null}
   ```
3. El botón de idioma se activa solo. Idiomas soportados: `es`, `en`, `pt`, `zh`.

## Nota
Si más adelante quieres una nueva tanda de episodios, crea `podcast-v2` y cambia
la constante `REL` en ambos HTML al nuevo tag.
