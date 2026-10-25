# Stack y herramientas revisadas · criterio de selección

| Capa | Elección MVP | Alternativas evaluadas y regla de adopción |
|---|---|---|
| Runtime y entorno | Python >=3.11; preferencia 3.12, venv/uv opcional | Fijar uv.lock una vez disponibles todos los paquetes y plataformas |
| Curación | JSONL + catálogo de procedencia + SHA-256 | ODCS/Pandera al escalar a corpus heterogéneo y ETL automatizado |
| Almacenamiento | SQLite FTS5 (stdlib, CPU) | DuckDB para observabilidad/evaluación; pgvector/Qdrant cuando volumen lo justifique |
| Recuperación | BM25/FTS5 + E5 multilingual-small opcional, RRF | CRAG/consulta correctiva solo si existen fuentes legales actualizables y criterio medido |
| Generación | Ollama qwen3:1.7b local opt-in | Modelo mayor solo tras medir calidad, memoria, latencia, costo y riesgos |
| Interfaz | Streamlit loopback, uso individual | FastAPI/MCP y despliegue solo tras seguridad y cumplimiento |
| Evaluación | pytest + hits + MRR + OOD; pruebas de seguridad | Ragas/DeepEval/Giskard al contar con corpus, ground-truth y revisión humana |
| Calidad | Ruff, pytest/JUnit, pip-audit, Bandit, Gitleaks | Quality gates ERL v2 antes de cualquier publicación |
| Auditoría IA | NIST AI RMF GenAI, OWASP LLM Top 10 2025 | Strix únicamente en sandbox autorizado de una superficie desplegada |
| Impacto y grafos | Mermaid + ADR, opcional Understand-Anything | Usar grafos de repositorio para cambios grandes, no para validar evidencias clínicas |
| Alto rendimiento | Baseline Python | Rust + PyO3 únicamente si un benchmark repetible demuestra cuello de botella |

### Justificación de free y local

- Software base Python+SQLite FTS5 no requiere pagos ni cuentas.
- Modelo semántico E5 MIT; se descarga solo si el usuario opta por búsqueda híbrida.
- Qwen3:1.7b publicado en Ollama con licencia Apache 2.0. Los pesos se descargan por separado, nunca dentro de este ZIP.
- Para 20 fichas, añadir un cluster vectorial y una base de datos externa sería complejidad innecesaria.
- **Free to read no equivale a open for AI ingestion**: cualquier extensión del corpus pasa por revisión específica de derechos.
