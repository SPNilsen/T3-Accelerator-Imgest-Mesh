# Role Profile — Writing

## Scope in this project
Heavy documentation footprint:
- MkDocs Material site (`mkdocs.yml`) with offline/PDF support, Mermaid diagrams, git-history plugin
- Pandoc-based HTML/PDF pipeline (`README-pandoc.md`) with LaTeX, crossref, MathJax

## Major sections under `docs/`
- `t3/` — project management artifacts (activity blog, FAQ, glossary, file maps)
- `crisp-dm/` — data science methodology guide
- `hpc/` — cluster, K8s, SLURM, GPU infrastructure docs
- `armor/` — J&J Vistakon ALI case study (binary + multi-class defect detection)
- `db/`, `dl/`, `gen/` — reference material (SQL/NoSQL, deep-learning templates, RAG)

## Conventions
- Hand-authored Markdown, no templating
- Assets in `docs/assets/`
- Generated output in `docs/generated/`

## Known drift
- Root `README.md` describes a `containers/ingest/preprocess/decision` directory layout that does not match the actual `resources/{camera,orchestrator,inference,webserver}` code. Worth fixing during `/wrap` of an early job.
