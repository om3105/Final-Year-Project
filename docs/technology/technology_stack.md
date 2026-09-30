# Technology stack research

This is a proposed stack, subject to the dataset and ₹0 deployment gates. Version pins belong in a future lockfile after environment testing, not in this research document.

| Tool | Purpose / selection | Alternative and limits | Cost / license |
|---|---|---|---|
| Python + PyTorch | Training and inference; matches reference implementations `[1]`, `[2]` | TensorFlow/JAX; GPU memory remains a constraint | Free, open source; verify exact package licenses on lock. |
| MONAI | Medical-image transforms, networks and evaluation utilities | Custom transforms; still need audit of spatial metadata | Free, Apache-2.0; [official docs](https://docs.monai.io/). |
| SimpleITK / pydicom | Medical image loading, orientation and metadata handling | nibabel for NIfTI; strip identifiers | Free open source; [SimpleITK](https://simpleitk.org/), [pydicom](https://pydicom.github.io/pydicom/stable/). |
| Hugging Face Transformers | Candidate pretrained tabular/text/vision modules where licenses and checkpoints permit | Native PyTorch modules may be lighter | Free library, Apache-2.0; models have individual licenses. |
| SHAP | Clinical feature attribution experiment `[2]` | Permutation importance; SHAP can be slow and unstable under correlation | Free, MIT; [docs](https://shap.readthedocs.io/). |
| FastAPI + Pydantic | Typed REST service and OpenAPI | Flask; CPU model load and upload limits require testing | Free, MIT; [FastAPI docs](https://fastapi.tiangolo.com/). |
| Next.js + React | Browser UI, routing and accessibility | Static React app; Next server features may complicate free hosting | Free, MIT; [Next docs](https://nextjs.org/docs). |
| Tailwind CSS | Optional design system utility | CSS modules; avoid adding it without component need | Free, MIT. |
| Git + GitHub | Version control and collaboration | GitLab; repo must exclude data/secrets | Free tier; [GitHub docs](https://docs.github.com/). |
| Google Colab Free | Browser-based exploratory training | Codespaces CPU, institutional compute | ₹0 target, dynamic GPU limits; [official FAQ](https://research.google.com/colaboratory/faq.html). |
| Hugging Face Hub | Versioned checkpoint repository, **if release is permitted** | GitHub Releases; private storage policy differs | Public storage best effort; [official limits](https://huggingface.co/docs/hub/storage-limits). |

Compatibility gate: Python version, PyTorch/CUDA wheel, MONAI/SimpleITK wheels, transformer checkpoint license, and model file format must be tested together in Colab and the selected inference host. Never assume a GPU at inference. Dataset use agreements supersede convenience of cloud tooling.
