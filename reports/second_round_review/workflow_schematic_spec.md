# Proposed computational workflow schematic

Purpose: address Reviewer #5 request for a schematic and correct the manuscript's practical positioning.

Recommended figure title: Computational workflow used in the proof-of-concept ADC conjugation-platform classifier.

Recommended panels / boxes:

1. Literature and CMC rationale
   - Select ADC conjugation-platform families.
   - Define synthetic ranges for DAR and developability/manufacturability features.
   - Important label: "assumption-driven synthetic ranges".

2. Synthetic dataset construction
   - 48 records total; six platforms; eight records per platform.
   - Numeric features: DAR_Mean, DAR_Std, DAR_CV, Homogeneity, Stability_Score, Expression_Ease, Cost_Index, Scalability, Latency_to_Clinic_yrs.
   - Categorical descriptors excluded from model fitting if target-revealing.

3. Preprocessing and model training
   - Train/test split and repeated stratified CV.
   - Models compared: Random Forest, Extra Trees, SVM, logistic regression, gradient boosting, decision tree, kNN, dummy baseline.

4. Internal model-quality audit
   - Hold-out uncertainty.
   - Repeated CV and nested CV.
   - Seed sensitivity.
   - Leave-one-platform-out stress test.
   - Redundant-feature ablation.
   - Noise / perturbation sensitivity.

5. Literature-derived 20-ADC stress test
   - Strict two-feature check: DAR_Mean + DAR_CV.
   - Partly harmonized five-feature check.
   - Applicability-domain/range screen.
   - Label clearly: "face-validity stress test, not external validation".

6. Intended use after revision
   - Early conjugation/characterization data entered by scientist.
   - Model returns candidate category/class plus caution flags.
   - Output supports documentation, comparison, and process-optimization discussion.
   - Label clearly: "not yet a prospective pre-experimental selector".

7. Required future validation
   - Independent industrial/experimental records.
   - Batch grouping by ADC.
   - Locked external cohort.
   - Prospective experimental validation.

Visual style: simple left-to-right flowchart. Avoid implying that the model has been validated prospectively. Use caution icons or grey boxes for limitations.
