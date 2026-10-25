# ADR-0001: RAG local, recuperador léxico base y embeddings opcionales

**Estado:** aceptado para MVP (20-10-2026).

**Contexto:** estudiantes de la salud con recursos limitados; corpus pequeño; prioridad a trazabilidad, licencias y seguridad.

**Decisión:** SQLite FTS5, corpus original curado, Ollama y E5 únicamente opt-in. Entregable ejecutable sin cuenta, clave API, GPU ni conexión después de instalar Python.

**Alternativas:** pgvector, FAISS, Chroma, Milvus, Qdrant, LlamaIndex/LangChain. Son útiles al crecer volumen/operación, pero innecesarios para solo 20 fichas; elevan complejidad y superficie de ataque.

**Caveats:** el MVP no comprueba equivalencia semántica entre respuesta y fuente; el umbral semántico de 0.50 es heurístico exploratorio (no clínicamente calibrado). Medir sensibilidad y calibración antes de publicar afirmaciones de precisión.

**Siguiente decisión:** comparar FTS5 vs E5 híbrido con conjunto de prueba congelado, medición de latencia, calidad por estrato y revisión humana ciega de seguridad.
