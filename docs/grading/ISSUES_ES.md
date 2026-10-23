# Textos de los issues públicos (para abrir en GitHub)

Los títulos y cuerpos van en inglés, porque el repositorio es público y lo revisarán en JOSS.

---

**#1 Grading layer 2: semantic linkage of O\*NET tasks to ESCO skills**
Link each of the 18,796 O\*NET 30.2 tasks to its closest ESCO v1.2.1 skills with sentence embeddings (bi-encoder retrieval with a relative percentile threshold, NLI re-ranking). Derive per-task features: share of knowledge concepts, share of social transversal skills, and share of digital (DigComp) competences. Pin the model revision, run on CPU, and deposit the embeddings. Success criterion: higher within-GWA variance of K than the structural prior (5.3 %) and better convergence of E with the Eloundou et al. human labels than ρ = 0.40.

**#2 Grading layer 3: anchor-based zero-shot scoring**
Score tasks against anchors derived from published definitions: the codified/uncodified information distinction of Fernández-Macías & Bisello (2022) for K, and the E0/E1/E2 rubric of Eloundou et al. (2024) for E. Use NLI models trained only on commercially usable data ("-c" variants). Report agreement with the external references.

**#3 Discriminant validation of K**
(a) Correlation of K with the non-routine analytical index within each Job Zone. (b) A new, dated hypothesis: K versus routine cognitive content within non-manual occupations only. Pre-register before running.

**#4 Composite and uncertainty (JRC-COIN)**
Normalisation, internal-coherence checks and aggregation of layers 1–3. Monte Carlo over method choices (formula weights, thresholds, embedding model) with Sobol sensitivity indices and median ranks with 5–95 % intervals per task.

**#5 Layer T pilot: vendor-capability corpus (finance and consulting)**
For the 967 software products used in the 27 pilot occupations (116 hot technologies), collect short capability statements from public vendor documentation, separating business software from embedded AI features. Each statement carries its URL, an archived snapshot and the access date, and is graded as vendor self-declaration. Match tasks to capabilities within each occupation (support / automate / AI). Public pages only; respect robots.txt and terms of use; quotes of at most 25 words.

**#6 Layer S: certifiable technical competence**
Build a corpus of public certification exam objectives (Microsoft, SAP, Oracle, IBM, Cisco, AWS) and of European frameworks (e-CF EN 16234-1, DigComp, ESCO). Compute, per task and technology, whether a recognised certification covers the competence, and the gap T × (1 − S).

**#7 Layer U: effective utilisation**
Tidy table of enterprise adoption of ERP, CRM, supply-chain integration and AI from Eurostat (isoc_eb_iip, isoc_eb_ics, isoc_eb_ai) by NACE sector, size class and country. Note that the headline aggregate excludes financial services (NACE K). Treat utilisation depth as a declared assumption (0.10–0.35, central 0.27) in the Monte Carlo.

**#8 Replace the legacy AXI grades in OAXI-EU (v4.1)**
Rebuild OAXI-EU from `itea.grading`, regenerate the outputs and the benchmark validation, and document the change in the CHANGELOG. The legacy grades remain in the repository for reproducibility of v4.0.

**#9 English versions of the grading methodology and validation results**

**#10 Correct the podcast pages**
The pages give the date and size of McKinsey's 2025 layoffs inconsistently with the cited sources. Correct them against primary sources, or remove the claim.

**#11 Run the R reference implementation in CI**
