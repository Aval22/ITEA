# Guía de Depósito en Zenodo — ITEA Framework v3.0

Manual operativo para obtener (o actualizar) un DOI citable para este repositorio
en [Zenodo](https://zenodo.org/), el repositorio abierto operado por el CERN
que JOSS utiliza como canal canónico de archivado.

Cubre dos escenarios:

- **A. Integración automática GitHub-Zenodo** (recomendada — un click, reproducible, asocia cada tag de git a un DOI nuevo automáticamente).
- **B. Subida manual vía la interfaz web de Zenodo o la API REST** (alternativa — útil si GitHub aún no es público o si el enlace GitHub-Zenodo falla).

> **Único requisito de JOSS:** cuando JOSS acepte el paper, el repositorio
> debe tener un depósito Zenodo cuya instantánea archivada coincida con el
> commit revisado exacto. JOSS **no emite el DOI** — lo emites tú, y se lo
> entregas al editor.

---

## 0. Dos DOIs que debes tener claros desde el principio

Zenodo emite dos DOIs relacionados para cualquier depósito que tenga más de una versión:

| Tipo de DOI | A qué resuelve | Dónde se usa |
|-------------|----------------|---------------|
| **Concept DOI** | Una página que *siempre apunta a la última versión*. Estable entre versiones. | `CITATION.cff`, `README*.md`, entrada bibliográfica "cite el software", badges genéricos del tipo "use este DOI". |
| **Version DOI** | La instantánea de una versión específica (p. ej. v3.0, v3.1, …). Se emite uno nuevo en cada release. | El formulario de envío de JOSS, `MANIFEST.json` para v3.0, cualquier referencia a un *estado reproducible específico*. |

El `CITATION.cff` actual declara `10.5281/zenodo.19578916` como concept DOI.
**Verifícalo** visitando <https://doi.org/10.5281/zenodo.19578916>. Si responde
404, trátalo como placeholder y sigue el escenario A o B para emitir los DOIs reales.

---

## A. Integración GitHub → Zenodo (recomendada)

Es la ruta que esperan los revisores de JOSS. Tiempo total: ~10 minutos.

### A.1 — Configuración única de la cuenta

1. Inicia sesión en <https://zenodo.org/> usando tu cuenta de **GitHub** (la misma que es propietaria de `Aval22/ITEA`). Esto crea automáticamente el enlace Zenodo↔GitHub.
2. Confirma tu ORCID en <https://zenodo.org/account/settings/profile/> — fíjalo a `0009-0003-1438-1633`. Hacerlo *ahora* significa que el ORCID quedará incrustado en la metadata de cada depósito futuro.

### A.2 — Activar el repositorio para archivado

1. Visita <https://zenodo.org/account/settings/github/>.
2. Localiza `Aval22/ITEA` en la lista. (Si no aparece, pulsa "Sync" y recarga.)
3. Activa el interruptor a **ON**. Desde ese momento, cada nuevo *release* de GitHub (no un tag, un *release*) se replicará a Zenodo y recibirá un DOI.

### A.3 — Añadir el fichero de metadata Zenodo

Coloca el `docs/zenodo_metadata.json` adjunto (vecino de esta guía) como
**`.zenodo.json`** en la raíz del repositorio. El bot de Zenodo lee ese
fichero para poblar la metadata del depósito automáticamente. Esquema de
referencia: <https://developers.zenodo.org/#representation>.

```bash
cp docs/zenodo_metadata.json .zenodo.json
git add .zenodo.json
git commit -m "ci: añadir metadata de depósito Zenodo"
git push
```

### A.4 — Cortar el release v3.0 en GitHub

1. Etiqueta el commit que quieres archivar: `git tag -a v3.0 -m "ITEA Framework v3.0"` y luego `git push origin v3.0`.
2. Ve a **Releases → Draft a new release** en GitHub.
3. Selecciona el tag `v3.0`, el título "ITEA Framework v3.0", y pega la entrada v3.0 del `CHANGELOG.md` como descripción.
4. Pulsa **Publish release**.
5. En ~60 segundos Zenodo crea el depósito. Recarga <https://zenodo.org/account/settings/github/> hasta que veas un badge verde con el nuevo DOI en la fila de `Aval22/ITEA`. Pulsa el badge — enlaza al version DOI; el concept DOI está a un click en la barra lateral derecha del depósito ("Cite all versions").

### A.5 — Retroalimentar los DOIs al repositorio

Una vez tengas los dos DOIs (sean `CONCEPT_DOI` y `V3_DOI` los valores obtenidos):

1. **`CITATION.cff`** — sustituye el concept DOI placeholder por `CONCEPT_DOI`.
2. **`README.md` / `README_ES.md` / `README_PT.md` / `README_ZH.md`** — sustituye la URL del badge de DOI.
3. **`MANIFEST.json`** — sustituye `doi_concept` por `CONCEPT_DOI` y añade `doi_version: "<V3_DOI>"`.
4. **`paper/paper.md`** — si citas el software en la bibliografía, apunta esa entrada a `CONCEPT_DOI`.
5. **`code/v3/itea_functions_v3.py`** y **`.R`** — actualiza el comentario `DOI:` de la cabecera.
6. Commit:

   ```bash
   git commit -am "docs: retroalimentar DOIs Zenodo (concept=$CONCEPT_DOI, v3.0=$V3_DOI)"
   git push
   ```

   Este commit **no** requiere un nuevo release — Zenodo ya archivó el commit anterior. Las futuras v3.1, v4.0 etc. heredarán automáticamente el mismo concept DOI.

---

## B. Subida manual (ruta alternativa)

Úsala solo si (i) el repositorio de GitHub aún no es público, (ii) quieres un depósito único independiente de GitHub, o (iii) la integración GitHub de Zenodo está fallando.

### B.1 — Construir el paquete de subida

```bash
cd "/ruta/a/Framework ITEA"
git archive --format=zip --prefix=ITEA-Framework-v3.0/ HEAD -o ../ITEA-Framework-v3.0.zip
```

Si el proyecto aún no está bajo git:

```bash
cd ..
zip -r ITEA-Framework-v3.0.zip "Framework ITEA" -x "*.DS_Store" -x "*/.*"
```

El ZIP resultante debe incluir `MANIFEST.json` para que cualquiera pueda
re-verificar la integridad de los ficheros frente a los digests SHA-256 tras la descarga.

### B.2 — Crear el depósito (interfaz web)

1. Visita <https://zenodo.org/uploads/new>.
2. Arrastra `ITEA-Framework-v3.0.zip` al área de subida.
3. Rellena el bloque de metadata con los valores de `docs/zenodo_metadata.json` (ver §C abajo).
4. Pulsa **Save** (crea el depósito) y luego **Publish** (emite el DOI). **Publish es irreversible** — revisa con cuidado antes.

### B.3 — Crear el depósito (API REST, opcional)

```bash
ZENODO_TOKEN="<token de acceso personal de https://zenodo.org/account/settings/applications/tokens/new/>"

# 1. Crear depósito vacío
DEPOSIT=$(curl -s -H "Authorization: Bearer $ZENODO_TOKEN" \
  -H "Content-Type: application/json" \
  -X POST "https://zenodo.org/api/deposit/depositions" -d '{}')

DEPOSIT_ID=$(echo "$DEPOSIT" | jq -r '.id')
BUCKET=$(echo "$DEPOSIT" | jq -r '.links.bucket')

# 2. Subir el ZIP al bucket del depósito
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
  -X PUT "$BUCKET/ITEA-Framework-v3.0.zip" \
  --upload-file ITEA-Framework-v3.0.zip

# 3. Empujar la metadata
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
  -H "Content-Type: application/json" \
  -X PUT "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID" \
  -d @docs/zenodo_metadata.json

# 4. Publicar (emite el DOI — irreversible)
curl -H "Authorization: Bearer $ZENODO_TOKEN" \
  -X POST "https://zenodo.org/api/deposit/depositions/$DEPOSIT_ID/actions/publish"
```

La llamada final `publish` devuelve un documento JSON que contiene los campos
`conceptdoi` y `doi`. Guárdalos — son los valores que necesitas para
retroalimentar según §A.5.

---

## C. Metadata requerida (única fuente de verdad)

Los campos siguientes son los que Zenodo *exige* (★) o *recomienda* (☆) para
un depósito de software. Viven en `docs/zenodo_metadata.json`.

| Campo | Valor | ¿Obligatorio? |
|-------|-------|---------------|
| `title` | ITEA Framework: A Multidimensional System for Measuring Occupational Exposure to Algorithmic Expropriation under the Agentic AI Regime | ★ |
| `version` | 3.0 | ★ |
| `publication_date` | 2026-04-30 | ★ |
| `upload_type` | software | ★ |
| `description` | (HTML permitido) Ver `zenodo_metadata.json` — abstract de `CITATION.cff` más un párrafo "qué cambia" y la correlación de validación frente a AIOE. | ★ |
| `creators[].name` | García-Lluis Valencia, Alberto | ★ |
| `creators[].orcid` | 0009-0003-1438-1633 | ☆ |
| `creators[].affiliation` | Universidad Rey Juan Carlos | ☆ |
| `license` | MIT | ★ |
| `access_right` | open | ★ |
| `keywords` | labor economics, automation, Agentic AI, occupational exposure, algorithmic expropriation, psychometric validation, O\*NET, AIOE | ☆ |
| `related_identifiers` | Papers de la trilogía (8A, 8B, 8C) por DOI; URL del repo de GitHub con relación `isSupplementTo`; el paper de JOSS una vez tenga DOI | ☆ |
| `communities` | (opcional) `joss` una vez aceptado por JOSS — Zenodo moverá el depósito a la comunidad JOSS | ☆ |
| `language` | eng (idioma del software/documentación principal) | ☆ |
| `notes` | "Concept DOI: <rellenar tras el primer publish>; Version DOI: <rellenar tras el primer publish>." | ☆ |

El `docs/zenodo_metadata.json` adjunto contiene ya todos los valores
anteriores formateados exactamente como espera la API REST de Zenodo.

---

## D. Tras la emisión del DOI — verificación rápida

```bash
# El concept DOI debe resolver a la última versión (v3.0 ahora mismo)
curl -sIL "https://doi.org/$CONCEPT_DOI" | grep -E "^location:"

# El version DOI debe resolver a una página de Zenodo cuya versión listada lea "3.0"
curl -sIL "https://doi.org/$V3_DOI" | grep -E "^location:"
```

Después, vuelve a calcular el SHA-256 del ZIP que sirve Zenodo y confirma que
los digests coinciden con `MANIFEST.json`:

```bash
curl -L -o /tmp/itea_v3.zip "https://zenodo.org/records/<RECORD_ID>/files/ITEA-Framework-v3.0.zip"
unzip -d /tmp/itea_v3 /tmp/itea_v3.zip
cd /tmp/itea_v3/ITEA-Framework-v3.0
python3 - <<'PY'
import json, hashlib, os
m = json.load(open("MANIFEST.json"))
for f in m["files"]:
    h = hashlib.sha256(open(f["path"], "rb").read()).hexdigest()
    print(("OK " if h == f["sha256"] else "DIFF "), f["path"])
PY
```

---

## E. Envío posterior a JOSS

1. Actualiza `paper/paper.md` y `CITATION.cff` con el **concept DOI** y el **version DOI** de v3.0.
2. Abre el formulario de envío de JOSS: <https://joss.theoj.org/papers/new>.
3. Aporta:
   - **Repository URL**: `https://github.com/Aval22/ITEA`
   - **Version**: `v3.0`
   - **Software DOI (concept)**: `<CONCEPT_DOI>`
   - **Software archive DOI (version)**: `<V3_DOI>`
4. El bot construirá `paper.pdf` desde `paper/paper.md`, validará el YAML y ejecutará un chequeo de citas. Resuelve cualquier flag y a continuación se asignará un editor humano.

---

## F. Versionado posterior (p. ej. v3.1)

Cuando cortes una release futura (v3.1):

1. `git tag -a v3.1 -m "ITEA Framework v3.1"` → `git push origin v3.1`.
2. Borrador de un nuevo release de GitHub como en §A.4 — Zenodo lo archiva automáticamente y emite un *version DOI nuevo* bajo el mismo *concept DOI*.
3. Actualiza badges y ficheros de citación para reflejar v3.1; el concept DOI **no cambia**.

---

## G. Glosario rápido (terminología Zenodo / JOSS)

| Término | Significado |
|---------|-------------|
| **Deposit** | Registro de Zenodo que agrupa fichero(s) + metadata. |
| **Concept DOI** | DOI estable que apunta siempre a la última versión del depósito. |
| **Version DOI** | DOI de una instantánea concreta (no cambia jamás una vez publicado). |
| **Reserve DOI** | Opción que permite saber el DOI antes de publicar (útil si quieres meterlo en `paper.md` antes del publish). |
| **Community** | Agrupación temática dentro de Zenodo (p. ej. `joss`, `eosc`, `nih`). |
| **Personal Access Token** | Token API generado en `zenodo.org/account/settings/applications/tokens/new/` con scopes `deposit:write` y `deposit:actions` para automatizar subidas. |
| **Sandbox Zenodo** | <https://sandbox.zenodo.org/> — entorno de pruebas idéntico a producción donde puedes ensayar la subida sin emitir DOIs reales. **Recomendado** para el primer ensayo. |
| **editorialbot (Whedon)** | Bot de JOSS que valida el YAML de `paper.md`, genera el PDF y comprueba citas. |

---

*Ficheros complementarios:*

- `docs/zenodo_metadata.json` — metadata legible por máquina para la API de Zenodo y `.zenodo.json`.
- `docs/JOSS_SUBMISSION_CHECKLIST.md` — auditoría más amplia de preparación para JOSS.
- `docs/DEPLOYMENT_REPORT_2026-05-07.md` — registro operativo del despliegue v3.0 con verificación SHA-256.
- `docs/ZENODO_DEPOSIT_GUIDE.md` — versión en inglés de esta misma guía.
