# Project roadmap

Each phase has an objective, input, output and acceptance gate. Implementation begins only after the pre-development review and explicit instruction.

| Phase | Objective | Inputs → outputs | Acceptance / dependency |
|---|---|---|---|
| 0 Research | Verify literature, dataset rights, design and feasibility | Sources → paper catalog and docs | 50 verified records; substantive notes and base comparison; unresolved issues declared. |
| 1 Dataset preparation | Obtain lawful paired cohort | Approved access → private manifest and aggregate cohort report | DUA/cloud review; no restricted data in Git; patient keys and label provenance checked. Depends 0. |
| 2 Baselines | Establish image-only, clinical-only, simple fusion | Approved cohort → baseline checkpoints/metrics | Fixed split, preprocessing tests and reproducible runs. Depends 1. |
| 3 Proposed model | Add cross-attention and optional Transformer | Baselines → candidate configs | Shape/mask tests, comparable parameter/compute accounting. Depends 2. |
| 4 Training | Train all pre-registered arms | Configs → checkpoints and run ledger | Seeds, stopping and hardware recorded. Depends 3. |
| 5 Evaluation | Locked patient-level test, calibration, external if possible | Frozen checkpoints → aggregate metrics | No leakage; per-class metrics and uncertainty. Depends 4. |
| 6 Explainability | Validate image/clinical attributions | Selected checkpoint → QA report | Method compatibility and stability checks. Depends 5. |
| 7 FastAPI | Add bounded inference API | Approved model → service | API/security tests; no PHI logging. Depends 5–6. |
| 8 Next.js | Build accessible research UI | API spec → screens | Synthetic-case usability/accessibility review. Depends 7. |
| 9 Cloud deployment | Test free host eligibility and resource fit | Service/UI → demo URL or documented fallback | ₹0, DUA/privacy approval, measured cold/warm latency. Depends 7–8. |
| 10 Testing | System and security regression | Components → test report | Passing required tests and threat checks. Depends 7–9. |
| 11 Documentation | Update reproducibility, model card, results | Artifacts → final docs | Every result traceable to config/cohort. Ongoing. |
| 12 Final demo | Guide walkthrough | Approved demo → presentation | Clear research-only messaging and limitations. Depends 0–11. |
