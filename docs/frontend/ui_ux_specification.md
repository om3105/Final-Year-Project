# Research web interface specification

The application is a **research prototype**. Persistent copy near upload and result actions: “AI-assisted prediction for research only. Not a medical diagnosis.” Do not imply clinical approval or treatment advice.

| Screen | Main content and components | States / API |
|---|---|---|
| Landing | Purpose, limitations, privacy notice, “New analysis”, model/version link | No patient data sent. |
| New analysis | Eligibility checklist, consent/authorized-data notice, supported MRI format, clinical schema summary | Disable submission until validation; link to model info. |
| MRI upload | Drag/drop and file picker, file size/type, de-identification reminder, local preview only if safe | Validation progress; unsupported/corrupt/too-large error. |
| Clinical information | Typed fields with units, unknown option, measurement-time help and source labels | Inline range and missingness errors; do not collect name, DOB or contact details. |
| Prediction result | Class probabilities, model version, QC state, uncertainty/abstention message, downloadable **non-identifying** summary only if permitted | `POST /api/analyze`; loading/cancel/retry; no diagnosis claim. |
| Explainability | Image overlay with source image, class selector, clinical contributions with feature source | `POST /api/explain`; lazy loading, timeout, “explanation unavailable”. |
| Analysis history | Default empty/disabled because no durable medical storage is approved | `GET /api/history` returns disabled/no stored cases until policy and auth are approved. |
| Model information | Cohort, split, metrics, limitations, calibration and model card | `GET /api/model`; versioned. |
| About / How it works | Plain-language diagram, intended users, dataset and paper attribution | Static. |
| Navigation | Clear routes, breadcrumbs, visible prototype label | Responsive desktop/tablet/mobile. |

Accessibility: semantic headings and labels, keyboard navigation, visible focus, text alternatives for overlays, color-independent legend, adequate contrast, screen-reader status announcements, and table alternatives for charts. Responsive MRI previews must preserve aspect ratio and orientation. Error copy tells the user what field/file to correct without repeating sensitive input. Loading indicates cold-start may be long and never silently re-submits. Browser history should avoid patient data in URLs; no analytics on upload/result paths.
