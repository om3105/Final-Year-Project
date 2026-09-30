# Mathematical formulation

For patient (i), let (X_i\in\mathbb{R}^{1\times D\times H\times W}) be a preprocessed T1 MRI, (c_i\in\mathbb{R}^{F}) the time-valid clinical vector, (m_i\in\{0,1\}^{F}) its observed-value mask, and (y_i\in\{1,\ldots,K\}) the diagnostic research label. (B) is batch size, (D,H,W) are voxel dimensions, (F) is feature count, (K) is class count, (d) is embedding width, and (N_I,N_C) are image and clinical token counts.

The image encoder yields (I_i=f_I(X_i)\in\mathbb{R}^{N_I\times d}). A feature tokenizer or clinical encoder yields (C_i=f_C(c_i,m_i)\in\mathbb{R}^{N_C\times d}). Missing clinical fields are masked, not set to semantically meaningful zero. The simple baseline is (z_i^{cat}=g([\operatorname{pool}(I_i);\operatorname{pool}(C_i)])), where (g) is an MLP.

For image-query cross-attention, (Q=I_iW_Q), (K_C=C_iW_K), (V_C=C_iW_V). Then

\[
A_{I\leftarrow C}=\operatorname{softmax}\left(\frac{QK_C^\top}{\sqrt{d_h}}+M_i\right)V_C,
\]

where (d_h) is head width and (M_i) contains (-\infty) at masked clinical-token positions. Multi-head outputs are concatenated and projected. A residual/layer-normalized state (H_i=\operatorname{LN}(I_i+\operatorname{MHA}(I_i,C_i))) may enter optional multimodal self-attention (T_i=\operatorname{Transformer}([H_i;C_i])). Pooling gives (z_i=\operatorname{pool}(T_i)). The comparison arm may pool (H_i) directly to isolate the added Transformer effect.

Logits are (\ell_i=W_oz_i+b_o\in\mathbb{R}^K); probabilities are (p_{ik}=\exp(\ell_{ik})/\sum_j\exp(\ell_{ij})). Training minimizes (L=-(1/B)\sum_i w_{y_i}\log p_{i,y_i}+\lambda\lVert\theta\rVert_2^2), where (w_k) are optional training-set class weights, (\theta) trainable parameters and (\lambda) regularization strength. A validation-only calibration map may transform logits before reporting probabilities.

An image attribution (E_I(X_i,k)) and clinical attribution vector (E_C(c_i,k)\in\mathbb{R}^F) are *method-dependent outputs* (e.g., gradient localization and SHAP), not terms in the class probability definition and not causal explanations. Output also includes model version, input QC status, and an out-of-distribution/abstention flag when defined.
