# REST API specification (planned, not implemented)

All endpoints are versioned under `/api`; JSON errors contain stable `code`, human-readable `message`, and request ID, with no raw clinical values or filenames. TLS is required in deployed environments. CORS allows only the configured frontend origin. Public inference remains disabled until data/privacy and resource gates pass.

| Endpoint | Request / response | Validation and errors | Model / latency |
|---|---|---|---|
| `GET /api/health` | No body; `{status, model_loaded, version}` | 200 healthy; 503 model unavailable | Lightweight; no patient information. |
| `GET /api/model` | No body; model card summary, classes, accepted modality/schema, version, limitations | 200; 503 if metadata unavailable | Static metadata; no checkpoint download. |
| `POST /api/analyze` | Multipart MRI file plus JSON clinical fields/measurement times; returns analysis ID (ephemeral), class probabilities, QC and abstention, model version | 400 malformed, 413 size, 415 type, 422 schema/QC, 429 rate, 503 model, 504 timeout | Full preprocessing and prediction; target latency to be measured. Do not persist input by default. |
| `POST /api/explain` | Ephemeral analysis token or same input under approved design; returns image overlay coordinates/asset and feature attributions | 404 expired token, 422 unsupported encoder/QC, 503/504 unavailable | Slower asynchronous option; never imply causal explanation. |
| `GET /api/history` | No body; `[]` plus `enabled:false` in default research mode | 401/403 if future authenticated history exists | No server-side history until retention/auth approval. |

Security: reject archives, polyglot files, unexpected transfer encoding, excessive dimensions and decompression bombs; inspect DICOM identifiers and never log payloads. Enforce request-size and per-origin rate limits. Model files are fixed/versioned and loaded read-only; no user-selectable filesystem path. Treat explanation artifacts as sensitive and delete on token expiry. A request ID is random and not a patient identifier. See [security](../security/security_and_privacy.md) and machine-readable [OpenAPI](openapi.yaml).
