# Technical feasibility review

**2026-09-29 assessment: partially feasible at ₹0.** Frontend, source control and browser-based development have credible free paths. A guaranteed live 3D MRI Transformer inference backend does not. Training may be possible intermittently on Colab Free, which explicitly does not guarantee GPUs or stable runtime limits ([official FAQ](https://research.google.com/colaboratory/faq.html)). A large image encoder plus tabular Transformer also risks GPU memory and small-cohort overfitting.

| Question | Finding / action |
|---|---|
| Train without local PC? | Potentially in Colab after dataset DUA/cloud security review; use frozen/small encoders and checkpoints. Not guaranteed. |
| Frontend free? | Vercel Hobby supports personal noncommercial projects with usage limits ([plan](https://vercel.com/docs/plans/hobby)). |
| Backend free? | Render Free is 0.1 CPU/512 MB and sleeps after 15 minutes; likely insufficient for full MRI Transformer ([compute](https://render.com/docs/compute-plans), [free plan](https://render.com/docs/free)). CPU Basic Spaces advertises 2 vCPU/16 GB but eligibility wording currently conflicts, so account provisioning must be tested ([Spaces](https://huggingface.co/docs/hub/spaces-overview)). |
| Model storage free? | Hugging Face public Hub storage is best effort; release may be constrained by dataset rights ([limits](https://huggingface.co/docs/hub/storage-limits)). |
| Free host sleeps? | Render wake-up is roughly a minute after 15 idle minutes; CPU Basic Spaces currently sleep after 48 hours inactivity. Cold model loading adds time. |
| Resource bottlenecks? | 3D MRI size, preprocessing, model RAM, attribution compute, cold-start and upload transfer. Benchmark before targets. |
| Free GPU absent? | Train CPU-feasible baselines, use intermittent Colab when available, reduce resolution/model size only if scientifically defensible. Do not promise full architecture training or live service. |
| History? | Durable free medical data storage is not authorized or designed; history disabled by default. |

The largest noncompute gate is dataset governance: [ADNI's DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf) constrains AI tools, cloud retention and public weights; [OASIS's DUA](https://bpb-us-e2.wpmucdn.com/sites.wustl.edu/dist/6/4383/files/2025/07/Data-Use-Agreement_July2025.pdf) limits disclosure and requires secure controlled storage. Cloud-only processing needs an approved design, not just a free account. A synthetic-only demo is the honest fallback until this is resolved.
