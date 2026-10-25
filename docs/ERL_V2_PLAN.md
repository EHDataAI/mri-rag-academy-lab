# ERL v2 · Quality gates y ejecución

**Meta del laboratorio:** recuperación de conocimiento educativo con fuentes, no consejo clínico.

| Etapa | Evidencia exigida | Estado inicial |
|---|---|---|
| L0 datos y derechos | Catálogo de derechos, texto original, URLs permitidas | Ejecutable |
| L0 integridad | Manifiesto SHA-256 y UTF-8 LF | Ejecutable |
| L1 software | Ruff completo, pytest, JUnit, compileall, git diff --check | Pendiente QA |
| L1 seguridad | CLI offline, bloqueo paciente-específico, URL loopback, gitleaks | Parte automatizada |
| L1 evaluación | Hit@3, MRR@3 y rechazo OOD, partición dev/test | Ejecución requerida |
| L2 científico | Revisión por TM RM, físico médico, tecnólogo/medicina y docente | NOT_RUN |
| L2 red-team | Revisión adversarial, jailbreak, prompt injection, contraste | Parcial |
| L2 despliegue | WCAG/manual UI, pentesting Strix en sandbox, cadena de suministros | NOT_RUN |

**Principios:** tests no equivalen a seguridad clínica; distinguir PASS/FAIL/NOT_RUN. Riesgo alto siempre prevalece sobre calidad promedio.

**Matriz del conjunto de evaluación:** 12 dev, 11 test incluidos 3 fuera de dominio. La partición es conceptual; este corpus pequeño no prueba generalización. No optimizar contra el test.

**Requisitos próximos:** revisión de contenido por expertos, medición del conjunto test bloqueado; Giskard/garak o Strix solo en laboratorio autorizado y aislado; evals adversariales multicapa; observabilidad sin almacenar preguntas clínicas.

**Nota de QA del entorno de construcción:** Python 3.13.5, pytest 9.0.2 disponibles. Ruff, Bandit, pip-audit, Streamlit y modelos semánticos/LLM no estaban disponibles; sus gates deben constar NOT_RUN, no PASS.
