# ₹0 deployment strategy (verified 2026-09-29)

**Assessment: partially feasible.** Browser-only development, Git hosting and a static research website can be free. Guaranteed always-on 3D MRI Transformer inference, durable history, private medical storage and free GPU are **not** established at ₹0.

| Service | Verified allowance | Material constraint |
|---|---|---|
| [Google Colab Free](https://research.google.com/colaboratory/faq.html) | Free interactive notebooks; GPU access sometimes available | GPU type, limits and runtime duration fluctuate; free sessions time out and are not deployment servers. |
| [GitHub Codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) | Personal GitHub Free: 120 core-hours and 15 GB-month | No guaranteed GPU; stop usage at included budget. |
| [Vercel Hobby](https://vercel.com/docs/plans/hobby) | Free personal, noncommercial Next.js hosting with listed usage limits | Function time/memory and noncommercial terms; no MRI inference there. |
| [Render Free](https://render.com/docs/free) | 750 instance-hours/workspace/month; idle spin-down after 15 min | [0.1 CPU/512 MB](https://render.com/docs/compute-plans), roughly minute-scale wake-up, ephemeral disk. Large models likely unsuitable. |
| [Hugging Face Spaces](https://huggingface.co/docs/hub/spaces-overview) | Docs list CPU Basic 2 vCPU/16 GB; 50 GB nonpersistent disk | Current page also says compute-backed Spaces may require a paid plan; verify account eligibility. [CPU Basic sleeps](https://huggingface.co/docs/hub/spaces-gpus) after inactivity (currently 48 h). No free GPU guarantee. |
| [Hugging Face Hub](https://huggingface.co/docs/hub/storage-limits) | Best-effort free public storage; limited private allocation | Public checkpoint release depends on dataset agreement and reconstruction-risk review. |

Architecture fallback: static Next.js UI on Vercel with synthetic demonstration cases; CPU inference only if a small verified checkpoint fits an eligible free host. If it does not, keep the backend local to an authorized cloud research session for guide evaluation and state clearly that public live inference is unavailable at ₹0. Do not use uptime pings to evade sleeping policies. A full live public medical-image service remains a feasibility risk, not a promise.

Free-tier pages can change. Recheck exact limits and eligibility before Phase 9. Protect against unexpected charges with provider spending caps and no paid upgrades. Uploaded patient images, clinical records and inference logs must never be sent to these services without explicit dataset and privacy authorization.
