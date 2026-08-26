# Manuscript text blocks for second-round revision

These are concise replacement/addition blocks to paste into the marked manuscript. They are written for a pharmaceutical journal audience, not a computational-methods journal. Add line numbers only after rebuilding the line-numbered DOCX.

## Abstract: replacement closing language

Recommended placement: final two sentences of Abstract.

> The literature-derived 20-ADC assessment was used as a face-validity stress test rather than as external validation of the trained model. Overall, the study provides an open, reproducible proof-of-concept workflow for organizing early ADC conjugation and characterization data, comparing platform-associated developability patterns, and identifying the data requirements needed before prospective platform selection can be validated experimentally.

## Introduction: positioning sentence

Recommended placement: end of Introduction.

> The present work should therefore be viewed as a proof-of-concept computational framework for post-characterization platform classification and decision support. It is not intended to establish a validated pre-experimental platform-selection model, because several required inputs are measured only after early conjugation and analytical characterization.

## Methods: dataset construction clarification

Recommended placement: Synthetic dataset subsection.

> The dataset was intentionally synthetic and balanced, with eight records generated for each of six conjugation platforms. Platform-specific numeric ranges were assigned for DAR_Mean, DAR_Std, DAR_CV, Homogeneity, Stability_Score, Expression_Ease, Cost_Index, Scalability, and Latency_to_Clinic_yrs. These ranges were selected to reflect expected qualitative differences among random lysine conjugation, cysteine-based approaches, and more controlled site-specific technologies; however, they were not fitted to confidential industrial batch records. As a result, the model learns from assumption-driven, class-conditioned distributions rather than from independent experimental CMC data.

## Methods: feature availability and units

Recommended placement: after feature list.

> DAR_Mean is reported as mol drug per mol antibody, DAR_Std in DAR units, DAR_CV as a unitless relative dispersion measure, and Latency_to_Clinic_yrs in years. Homogeneity, Stability_Score, Expression_Ease, Cost_Index, and Scalability are dimensionless normalized scores from 0 to 1 in the synthetic dataset. In a real ADC program, DAR_Mean, DAR_Std, DAR_CV, Homogeneity, and Stability_Score would usually become available only after early conjugation and analytical characterization. Thus, the current workflow is better positioned as an early process-optimization and decision-documentation aid than as a tool for choosing a platform before any experimental work.

## Methods: preprocessing and leakage control

Recommended placement: model training subsection.

> Model fitting used numeric developability and manufacturability descriptors only. Target-revealing categorical descriptors, including Platform, Vendor, Approved_Usage, and CMC_Risk, were not used as model inputs. The main internal task was six-class platform classification using the synthetic platform labels. Additional analyses removed collinear or redundant variables and examined whether internal performance was sensitive to train/test split, model class, and omitted platform family.

## Methods: literature assessment clarification

Recommended placement: literature-derived assessment subsection.

> The 20-ADC literature-derived assessment was not treated as external validation. Published ADC records did not consistently provide all nine synthetic-model inputs, and several available values fell outside the synthetic training range. Therefore, two stress tests were reported: a strict two-feature check using DAR_Mean and DAR_CV, and a partly harmonized five-feature check using DAR_Mean, DAR_CV, Stability_Score, Homogeneity, and Scalability where these could be assigned from literature-curated information. Because literature records more reliably support broad technology categories than exact six-platform labels, these checks were performed at the category level.

## Results: hold-out accuracy caution

Recommended placement: start of model performance Results.

> The original Random Forest hold-out split classified all 10 held-out synthetic records correctly. Because this test set was small, the corresponding Wilson 95% confidence interval remains wide, and the result should not be interpreted as evidence of generalizability. Repeated cross-validation, nested cross-validation, seed sensitivity, and leave-one-platform-out analyses provided a more conservative picture of model behavior.

## Results: Table II lead-in

Recommended placement: before Table II.

> Table II summarizes the revised model-quality audit. Across repeated stratified cross-validation, Random Forest accuracy was approximately 0.83 and macro F1 approximately 0.81, rather than the apparent 1.00 obtained in one small hold-out split. Seed sensitivity showed that perfect hold-out splits occurred for some random seeds but were not stable. Leave-one-platform-out testing further showed weak transfer for some platform families, especially when the omitted platform belonged to a technology category absent from training.

## Results: collinearity and feature ablation

Recommended placement: feature interpretation Results.

> Expression_Ease and Cost_Index were nearly collinear because the synthetic Cost_Index was constructed as an inverse manufacturability proxy. Removing Cost_Index, and then removing both Cost_Index and DAR_Std, did not materially reduce repeated-CV accuracy. Feature-importance and SHAP analyses were therefore interpreted as descriptions of the synthetic benchmark structure rather than as independent evidence that these variables are causal drivers of real ADC platform choice.

## Results: literature stress test

Recommended placement: 20-ADC Results.

> The revised literature-derived assessment did not reproduce the previously reported rule-based 19/20 concordance as a model-validation result. In the strict objective check using only DAR_Mean and DAR_CV, the trained Random Forest agreed with the reported technology category for 4 of 20 ADC programs. In the partly harmonized five-feature check, agreement increased to 16 of 20 programs. These results are reported as face-validity stress tests only. They show how the workflow behaves when applied to incomplete literature records, but they do not establish external performance.

## Results: applicability-domain warning

Recommended placement: after Figure 4 / Table III.

> Applicability-domain screening supported this cautious interpretation. Six of 20 literature records were outside the synthetic training range for DAR_Mean, 16 of 20 for DAR_CV, 16 of 20 for Stability_Score, and 2 of 20 for Homogeneity. These range mismatches indicate that the synthetic benchmark does not yet cover the full variability of published ADC programs.

## Discussion: practical use case

Recommended placement: practical use subsection.

> In its current form, the framework is most useful after an ADC team has generated early conjugation and characterization data. A CMC or developability scientist could enter measured DAR distribution, relative homogeneity, early stability, and process-feasibility descriptors to compare how the candidate resembles synthetic profiles associated with different platform families. The output should support structured discussion, documentation, and prioritization of follow-up experiments. It should not replace expert review, multi-criteria decision analysis, or prospective experimental confirmation.

## Discussion: transfer/federated learning future direction

Recommended placement: future work subsection.

> Future versions could use transfer learning or privacy-preserving federated learning to incorporate confidential industrial ADC datasets without requiring companies to pool raw records. Such approaches would only be meaningful after common feature definitions, assay conditions, endpoint labels, batch grouping rules, and locked external test cohorts are established. They would not remove the need for prospective experimental validation.

## Discussion: limitations paragraph

Recommended placement: limitations subsection.

> The main limitation is that the model was trained on 48 synthetic, balanced, class-conditioned records. The dataset was designed to test workflow feasibility and explainability, not to represent the full variability of industrial ADC CMC development. Performance metrics, SHAP values, and feature rankings may therefore partly reflect assumptions used during dataset construction. The 20-ADC literature assessment is incomplete, partly out-of-domain, and category-level; it should be viewed as a stress test and not as external validation.

## Conclusion: replacement

Recommended placement: Conclusion.

> This study establishes an open proof-of-concept workflow for ADC conjugation-platform classification using synthetic developability and manufacturability descriptors. The revised analyses show that the original perfect hold-out performance was optimistic and split-sensitive, while repeated cross-validation, platform-transfer testing, feature-ablation analysis, and literature-derived stress testing provide a more cautious assessment. The framework may be useful for organizing early characterization data and supporting CMC discussion, but prospective validation with independent experimental or industrial ADC records is required before it can be used for real platform-selection decisions.

## Table II caption: replacement

> Table II. Revised internal model-quality audit of the synthetic benchmark. The table reports the original hold-out result alongside repeated cross-validation, nested cross-validation, seed sensitivity, leave-one-platform-out transfer, and redundant-feature sensitivity analyses. All analyses are internal synthetic-data audits and do not establish external ADC-program performance.

## Table III caption: replacement

> Table III. Literature-derived 20-ADC stress tests. The strict objective check used only DAR_Mean and DAR_CV. The partly harmonized check used DAR_Mean, DAR_CV, Stability_Score, Homogeneity, and Scalability where these features could be assigned from literature-curated information. The table reports face-validity stress tests and applicability-domain warnings; these results are not external validation of the trained model.

## New workflow figure caption

> Figure X. Computational workflow for the proof-of-concept ADC conjugation-platform classifier. Platform-specific synthetic feature ranges were used to generate a balanced 48-record benchmark. Numeric descriptors were used for model training and internal auditing, including repeated cross-validation, nested cross-validation, seed sensitivity, leave-one-platform-out transfer, redundant-feature sensitivity, and perturbation/noise stress testing. A separate 20-ADC literature-derived assessment was used only as a face-validity stress test because published records were incomplete and partly outside the synthetic training range. The intended use is post-characterization decision support during early process optimization, not validated pre-experimental platform selection.
