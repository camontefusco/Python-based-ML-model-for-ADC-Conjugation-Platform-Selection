# Response to Reviewers - second revision skeleton

Note: fill line numbers only after the marked manuscript is rebuilt. Keep responses concise and avoid over-arguing.

## Opening paragraph

We thank the Editor and Reviewers for the careful reassessment of the revised manuscript. We have made additional changes to clarify the proof-of-concept nature of the work, the synthetic construction of the dataset, the limits of the internal performance metrics, and the distinction between model testing and literature-derived stress testing. Changes are marked in the revised manuscript.

## Reviewer #3

### Major point: Synthetic dataset construction and representativeness

Response draft: We agree that the synthetic dataset cannot be treated as representative industrial ADC CMC data. We revised the Methods to describe how the feature ranges were assigned by platform, how the 48 records were generated, and why this creates class-conditioned structure. We also added a predictor-variable table defining units, practical meaning, and when each feature would normally become available. The manuscript now states that the data support proof-of-concept method development only and not a validated predictive claim.

Manuscript changes to cite: Methods, dataset construction; new/expanded predictor-variable table; Discussion limitations. Lines: [add after rebuild].

### Major point: Hold-out performance and uncertainty

Response draft: We agree that the original 10/10 hold-out result could be misleading if presented alone. We revised the Results to report the Wilson confidence interval and to place that result beside repeated stratified CV, nested CV, seed sensitivity, leave-one-platform-out testing, and redundant-feature ablation. These analyses show that the 1.00 hold-out result is split-sensitive and should not be interpreted as evidence of generalizability.

Manuscript changes to cite: Results/Table II; Discussion. Lines: [add after rebuild].

### Major point: 95% concordance / rule-based classifier versus trained model

Response draft: We clarified this throughout the manuscript. The previously reported 19/20 threshold-rule result is no longer presented as external validation of the trained Random Forest. The revised Table III separates trained-model literature stress tests from the superseded rule-based assessment and describes the 20-ADC analysis as face-validity stress testing only.

Manuscript changes to cite: Abstract; Results/Table III; Discussion; Conclusion. Lines: [add after rebuild].

### Major point: Six-class training versus three-category literature assessment

Response draft: We added text explaining that the internal model was trained on six synthetic platform classes, while the literature-derived ADC records often support only broader technology-category assignment. Therefore, the 20-ADC assessment was performed at category level and is not directly comparable to the six-class internal task.

Manuscript changes to cite: Methods/validation section; Table III caption. Lines: [add after rebuild].

### Major point: Feature construction, collinearity, feature importance

Response draft: We identified Expression_Ease and Cost_Index as nearly collinear and added the rationale for removing Cost_Index in a sensitivity analysis. We also revised the interpretation of feature-importance and SHAP results to state that they reflect structure in the synthetic dataset and should not be treated as independent biological or manufacturing evidence.

Manuscript changes to cite: Methods/features; Results/feature ablation; Discussion/explainability. Lines: [add after rebuild].

### Minor points

Response draft: We revised terminology around validation, face validity, and concordance; softened language around 1.00 accuracy; clarified when input variables become available; and revised the Abstract so the literature stress test is not described as confirming Random Forest validity.

Manuscript changes to cite: Abstract; Methods; Results; Discussion; Conclusion. Lines: [add after rebuild].

## Reviewer #4

### Point 1: Table II readability

Response draft: We replaced Table II with a simplified model-quality audit table. The revised table separates the analysis type, model/feature set, metric, estimate, uncertainty/comparison, and interpretation.

Manuscript changes to cite: Table II. Lines: [add after rebuild].

### Point 2: Table III superseded 19/20 assessment

Response draft: We agree. The withdrawn 19/20 rule-based result is no longer mixed with the revised trained-model stress tests in Table III. The table now focuses on the strict two-feature and harmonized five-feature Random Forest literature checks plus an applicability-domain screen. The prior rule-based result is mentioned only as a superseded descriptive check where needed.

Manuscript changes to cite: Table III; Results text. Lines: [add after rebuild].

### Point 3: Keywords

Response draft: We replaced the generic keyword "Drug Development" with more specific ADC/CMC/model-validation terms.

Manuscript changes to cite: Keywords file. Lines: [add after rebuild].

## Reviewer #5

### Point 1: Workflow schematic

Response draft: We added a computational workflow schematic showing synthetic dataset generation, preprocessing, model training, internal audit, literature stress testing, decision-support output, and required future validation.

Manuscript changes to cite: New workflow figure and caption. Lines: [add after rebuild].

### Point 2: Units

Response draft: We added units or scales for all predictor variables and clarified which variables are dimensionless normalized scores.

Manuscript changes to cite: Methods and predictor-variable table. Lines: [add after rebuild].

### Point 3: Feature perturbation sensitivity

Response draft: We added/referenced synthetic perturbation testing to show how performance changes when feature values are perturbed. We present this as stress testing of a synthetic model, not as evidence of real-world validation.

Manuscript changes to cite: Table II; Methods/Results. Lines: [add after rebuild].

### Point 4: Predictor variable table

Response draft: We added a table defining each predictor, its units/scale, practical pharmaceutical meaning, and when it would normally become available in an ADC workflow.

Manuscript changes to cite: Predictor-variable table. Lines: [add after rebuild].

### Point 5: Transfer learning/federated learning

Response draft: We added a short future-directions paragraph noting that transfer learning or federated learning may eventually help integrate confidential industrial datasets, but only after harmonized feature definitions, locked endpoints, batch grouping, and independent validation are established.

Manuscript changes to cite: Discussion/future work. Lines: [add after rebuild].

### Practical positioning point

Response draft: We revised the manuscript to clarify that the current tool uses variables available after early conjugation and characterization. It is therefore positioned as a decision-support and documentation aid during early process optimization, not as a fully prospective pre-experimental platform-selection model.

Manuscript changes to cite: Abstract; Methods/use case; Discussion; Conclusion. Lines: [add after rebuild].
