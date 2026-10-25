# MRI-RAG Academy · ERL v2 · QA de construcción RC0

**Fecha de ejecución:** 2026-10-20. **Entorno verificado:** Linux, Python 3.13.5, pytest 9.0.2.

| Gate | Resultado | Evidencia |
|---|---|---|
| Carga y metadatos corpus | PASS | 20 fichas; 14 referencias; IDs y dominio HTTPS controlados |
| SHA-256 corpus | PASS | cards.jsonl y sources.json coinciden con manifest.json |
| SQLite FTS5 build | PASS | Índice de 20 fichas creado en local_data (no empaquetado) |
| QA pytest | PASS | 31/31 tests (tiempo <1 s), incluye seguridad básica y regresión |
| compileall Python | PASS | src, tests, app, scripts |
| CLI respuesta DWI/ADC | PASS | Consulta respondida con fichas/citas en modo extractivo |
| Evaluación test (8 respondibles, 3 OOD) | PASS TÉCNICO / NO VALIDACIÓN | Hit@3=1.0, MRR@3=1.0, abstención OOD=1.0 |
| Ruff y Ruff format | NOT_RUN | Ruff no instalado en entorno aislado; instalación sin red falló |
| Bandit / pip-audit / Gitleaks | NOT_RUN | Herramientas no disponibles |
| UI Streamlit | NOT_RUN | Streamlit no instalado; UI requiere verificación manual/WCAG |
| Embeddings E5 / modelo Ollama | NOT_RUN | Modelos y dependencias no descargados |
| Revisión clínica independiente | NOT_RUN | Fichas requieren revisión humana por TM RM + físico médico/docente |
| Auditoría externa y pen test aislado | NOT_RUN | Pendiente posterior a preparación del entorno |

## Interpretación correcta

El test fue escrito con vocabulario muy cercano al corpus original. Los tres ejemplos OOD son claramente ajenos a la RM. **Los valores 1.0 no demuestran generalización, calibración, fidelidad generativa, robustez ni seguridad del sistema.** Requiere un set congelado independiente, preguntas parafraseadas, casos adversariales, distractores, negativa a recomendaciones clínicas y peer review.

## Decisión de release

**RC0 = APTO PARA REVISIÓN LOCAL; BLOCK para despliegue público o uso educativo institucional hasta cerrar gates.**
