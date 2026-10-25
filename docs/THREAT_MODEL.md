# Threat model: tutor educativo MRI-RAG

**Alcance:** un usuario local, un corpus controlado y modelos solo en loopback. No desplegar públicamente en este estado.

| Riesgo (OWASP LLM 2025) | Ataque / fallo | Control actual | Brecha pendiente |
|---|---|---|---|
| LLM01 Prompt injection | Consulta o contexto intenta alterar instrucciones | Bloqueo básico de patrones y corpus solo de autores | Pruebas adversariales multilingües y contenido malicioso indirecto |
| LLM02 Information disclosure | Exposición de datos personales o registros sensibles | Sin carga de archivos ni datos clínicos; no logs de preguntas | Revisión de telemetría e infraestructura si se despliega |
| LLM03 Supply chain | Dependencias y modelos comprometidos | Funcionalidad stdlib por defecto; modelos opt-in | Lockfile, SBOM, hashes de pesos, pip-audit y firma de artefactos |
| LLM04 Data poisoning | Alteración del corpus | Manifiesto de hashes y esquema/hosts de fuentes | Firma de manifest, revisión editorial, controles de contribución |
| LLM05 Output handling | Cita falsa o decisión médica insegura | Citas regex válidas, fallback extractivo, aviso educativo | Verificación de cada afirmación, revisión de contenido de seguridad |
| LLM08 Embedding weakness | Recuperación de ficha incorrecta | Recuperación FTS5 base; RRF opcional | Calibración por consultas difíciles, pruebas de similitud adversarial |
| LLM09 Misinformation | Respuesta incorrecta con cita verosímil | Fichas originales, fuentes nombradas y límite de alcance | Peer review clínica, entailment, benchmarking independiente |
| LLM10 Unbounded consumption | Consultas grandes / consumo ilimitado de recursos | 1.500 caracteres, 300 tokens generados, timeout 45s | Rate limiting y cuotas al desplegar |

**Nota legal Chile:** la Ley 21.719 establece entrada en vigor 1 de diciembre de 2026. El prototipo evita datos personales, pero no se declara cumplimiento normativo certificado. Si se agregan cuentas, telemetría, perfiles o expedientes, se deberá realizar un análisis jurídico y técnico específico.

**Marcos:**
- OWASP Gen AI Security Project, Top 10 LLM 2025: https://genai.owasp.org/llm-top-10/
- NIST AI 600-1, Generative AI Profile: https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence
- BCN, Ley 21.719, 01-12-2026: https://www.bcn.cl/leychile/Navegar?idNorma=1209272&idParte=10527471&idVersion=2026-12-01

**Proceso posterior:** activar Strix solo con aplicación aislada, autorización explícita y superficie delimitada. Strix no reemplaza pruebas de calidad médica ni control bibliográfico. Understand-Anything sirve para inspeccionar grafo de dependencias del código, no para justificar hechos clínicos. La implementación en Rust/PyO3 queda supeditada a perfilado y métricas de cuello de botella, no es necesaria para 20 fichas.
