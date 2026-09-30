# Cloud data-use review for restricted MRI and clinical data

**Prepared 30 September 2026. Decision: no service approved for restricted participant data.** This is a research-team decision record template, not legal advice or provider approval. The authorized investigator and institution must assess the exact account and contract before data transfer.

## Source requirements

The [ADNI DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf) prohibits participant-level redistribution. Its AI appendix permits analysis by tools that guarantee safeguarded, contained inputs, warns against third-party long-term retention or public-model training, says opt-out alone is insufficient, requires review of remote compute terms, and calls for reconstruction-risk review before public weight release. It does **not** amount to a blanket ban on research model training. The [OASIS DUA](https://bpb-us-e2.wpmucdn.com/sites.wustl.edu/dist/6/4383/files/2025/07/Data-Use-Agreement_July2025.pdf) has separate named-user, sharing and storage restrictions. Passing ADNI review would not automatically pass OASIS review.

## Google Colab Free: current evidence and decision

The [Colab FAQ](https://research.google.com/colaboratory/faq.html) confirms free interactive compute with fluctuating limits, notebooks stored in Google Drive, account-private virtual machines that are eventually deleted, and notebook sharing that includes saved text and outputs. It also says Colab's **generative AI features** collect prompts, related code and generated output for product improvement, with possible human review and retention. Consequently, do not enter ADNI or OASIS participant data, identifiers, file paths, row-level outputs or derived examples into Colab AI prompts. Disabling or avoiding AI prompts is necessary but **does not by itself prove** that ordinary Colab compute or Drive storage satisfies a dataset DUA. The public FAQ does not establish a project-specific containment guarantee or institutional approval. **Colab restricted-data status: UNAPPROVED / UNVERIFIED.** Synthetic data are permissible for design work.

| Review question | Required evidence before restricted use |
|---|---|
| Who operates the compute and storage? | Exact provider, account class, institution ownership, terms/version, region if material, and access-control owner. |
| Is participant content retained, shared, used for provider training, or visible to other parties? | Contract/terms and provider documentation addressing input, outputs, runtime files, logs, backups, Drive and AI features. An “opt-out” alone is insufficient under ADNI's appendix. |
| What is the data path? | Source download → controlled storage → runtime → temporary files → notebooks/outputs → checkpoints → deletion, including automatic sync and backup. |
| Can unauthorized users or tools see data? | Named-user permissions, sharing defaults, notebook-output handling, secrets management, assistant integrations and incident response. |
| What leaves the environment? | Aggregate metrics only by default. Review checkpoint weights for extraction/reconstruction risk and source permission before publication. |
| Is ₹0 feasible under these terms? | Actual eligible free service, storage and runtime limits; do not presume free GPU or a permanent backend. |

## Disposition

- **Public GitHub/Codex prompts:** reject for raw or participant-level restricted data.
- **Colab Free/Drive:** hold for restricted data until investigator/institution confirms applicable terms and controls. Avoid its generative AI features for restricted material.
- **Public model Hub or web inference:** hold until checkpoint and upload/privacy reviews are complete.
- **Synthetic fixtures and aggregate documentation:** may proceed without dataset approval, provided they contain no real participant records.

The review sign-off must identify the investigator, reviewer, decision date, provider terms/version, approved data classes, approved services, retention/deletion, checkpoint policy and evidence location. Store signed evidence privately. Put only “approved”, “rejected”, or “pending” and a non-sensitive reference in the public [readiness record](../project/implementation_readiness.md).
