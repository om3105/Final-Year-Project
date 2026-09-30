# Browser-only development workflow

1. Create a personal GitHub account/repository and use browser editing or GitHub Codespaces within the documented free quota. Set a zero-spend limit. Keep source, tests and **aggregate** results in Git; never add restricted datasets or secrets.
2. Use a Google Colab notebook only after the chosen dataset DUA permits its security/retention model. Clone the Git repository in the ephemeral runtime, install pinned packages, retrieve authorized data to an access-controlled location, run experiment configs, and export aggregate metrics and a reviewed checkpoint. Record runtime type and package lock. Colab free GPU and uptime are not guaranteed.
3. Store an approved checkpoint in a versioned model repository only after checking data-use terms and extraction risk. Use a checksum and model card. Do not publish raw participant examples.
4. Build the UI in Codespaces. Deploy a research-only static or server-rendered frontend on an eligible free host. Deploy inference only after resource and privacy tests; a synthetic demo remains the safe fallback.
5. A new developer reads AGENTS.md, README.md, architecture, requirements and relevant research. They obtain their own authorized data access rather than asking another developer to share participant files.

Official allowance sources: [Colab FAQ](https://research.google.com/colaboratory/faq.html), [Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces), and [ADNI DUA](https://adni.loni.usc.edu/wp-content/themes/adni_2023/documents/ADNI_Data_Use_Agreement.pdf). Browser-only access does not remove dataset privacy duties.
