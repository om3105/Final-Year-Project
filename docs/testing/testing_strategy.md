# Testing strategy (for implementation phases)

Tests should check meaningful failure modes, not mirror code. Use synthetic medical-image fixtures and invented clinical values in CI; no restricted records.

| Layer | Required checks |
|---|---|
| Data validation | DICOM/NIfTI signature, dimensions, orientation, voxel spacing, de-identification, malformed and decompression-bomb rejection. |
| Preprocessing | Fit transforms on train fold only; fixed spatial transform and inverse alignment; missing clinical values distinct from zero. |
| Leakage | Participant/scan/visit/hash overlap checks, repeated slices grouped, label-time and feature-provenance audit. |
| Model | Tensor shapes, masks, all-missing branch, deterministic inference, checkpoint compatibility and abstention. |
| Inference/API | Contract/status-code tests, upload bounds, timeouts, concurrent requests, no payload in logs. |
| Frontend | Keyboard path, labels, loading/empty/error states, responsive layout, non-diagnosis copy. |
| Integration | Synthetic upload → prediction → attribution with model/version consistency and cleanup. |
| Security | Path traversal, polyglot file, rate limit, CORS/auth, secret scanning and dependency review. |
| ML regression | Fixed small synthetic benchmark; locked patient-level metric computation and calibration code; no expected clinical scores hard-coded. |

Before deployment, perform a manual threat and accessibility review and benchmark warm/cold CPU latency on the actual free host. Any real-data evaluation runs in an authorized controlled environment and exports aggregate results only.
