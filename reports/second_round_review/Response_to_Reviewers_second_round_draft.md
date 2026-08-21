# Response to Reviewers - second-round draft

Note: line numbers must be added after the revised, marked, line-numbered manuscript is generated.

Dear Editor and Reviewers,

Thank you for the additional review of the revised manuscript. We have further revised the manuscript to clarify the proof-of-concept nature of the work, the construction and limitations of the synthetic dataset, the uncertainty around model-performance metrics, and the distinction between internal model auditing and the literature-derived 20-ADC stress test. We also revised the tables, added clearer predictor definitions and units, and added a computational workflow schematic.

## Reviewer #3

### Major comment 1: Synthetic dataset construction and representativeness

We agree. The revised manuscript now states more directly that the 48-record dataset is synthetic, balanced, and class-conditioned. We expanded the Methods to explain that platform-specific ranges were assigned for DAR_Mean, DAR_Std, DAR_CV, Homogeneity, Stability_Score, Expression_Ease, Cost_Index, Scalability, and Latency_to_Clinic_yrs. We also added that these values were not fitted from industrial batch records and therefore cannot be considered representative of real industrial CMC variability.

Changes made: Methods, dataset construction section; predictor-variable table; Discussion limitations. Lines: [to add].

### Major comment 2: Hold-out performance and uncertainty

We agree that the original 1.00 hold-out accuracy could be misleading if shown alone. We revised the Results and Table II so that the original 10/10 hold-out result is presented together with its uncertainty and with repeated cross-validation, nested cross-validation, seed sensitivity, leave-one-platform-out transfer, and redundant-feature sensitivity analyses. These analyses show that the apparent perfect hold-out result is split-sensitive and should not be interpreted as external generalization.

Changes made: Results and Table II; Discussion. Lines: [to add].

### Major comment 3: 95% concordance and rule-based classifier

We clarified that the previously reported 19/20 rule-based concordance was not external validation of the trained Random Forest model. In the revised manuscript, the literature-derived assessment is described as a face-validity stress test only. The revised Table III reports the trained-model strict two-feature check and partly harmonized five-feature check, and the prior threshold-rule result is no longer mixed with those model results.

Changes made: Abstract; Results; Table III; Discussion; Conclusion. Lines: [to add].

### Major comment 4: Six-class training versus three-category literature assessment

We added text explaining that the synthetic benchmark used six named platform classes, whereas the literature-derived ADC records more consistently support broader technology categories. For this reason, the 20-ADC literature assessment was performed at category level and is not directly equivalent to the internal six-class synthetic benchmark.

Changes made: Methods, literature-derived assessment section; Table III caption. Lines: [to add].

### Major comment 5: Feature construction, collinearity, and interpretation

We identified Expression_Ease and Cost_Index as the nearly collinear variables. Cost_Index was constructed as an inverse cost/manufacturability proxy, which explains the correlation. We added a redundant-feature sensitivity analysis showing that removing Cost_Index, and then removing both Cost_Index and DAR_Std, did not materially reduce repeated-CV performance. We also softened the interpretation of SHAP and feature-importance results so they are presented as describing the synthetic benchmark rather than proving real-world biological or manufacturing drivers.

Changes made: Methods feature definitions; Results feature-ablation section; Discussion explainability limitations. Lines: [to add].

### Major comment 6: Graphical abstract and model inputs

We revised the description of the workflow and predictor inputs so that the graphical abstract and manuscript no longer imply that all inputs are available before experimental work. The revised text clarifies that several inputs are measured after early conjugation and characterization.

Changes made: Graphical abstract description; Methods; Discussion practical use. Lines: [to add].

### Minor comments

We revised the wording around validation, face validity, and concordance; softened statements about the 1.00 hold-out accuracy; clarified the synthetic-data limitations; explained when the input variables would become available for a new ADC; and revised the Abstract so the literature-derived stress test is not described as confirmation of the trained Random Forest model.

Changes made: Abstract; Methods; Results; Discussion; Conclusion. Lines: [to add].

## Reviewer #4

### Comment 1: Table II readability

We agree. Table II has been replaced with a cleaner model-quality audit table. The revised table separates the analysis type, feature set/model, metric, estimate, uncertainty/comparison, and interpretation.

Changes made: Table II. Lines: [to add].

### Comment 2: Table III and withdrawn 19/20 result

We agree. The withdrawn 19/20 threshold-rule result is no longer presented in the same way as the revised trained-model stress tests. Table III now focuses on the strict two-feature trained-model check, the partly harmonized five-feature trained-model check, and the applicability-domain screen. The prior rule-based result is mentioned only as a superseded descriptive check, not as model validation.

Changes made: Results; Table III; Table III caption. Lines: [to add].

### Comment 3: Keywords

We replaced the generic keyword “Drug Development” with more specific terms related to ADCs, conjugation platform selection, CMC developability, drug-to-antibody ratio, model validation, and machine learning.

Changes made: Keywords. Lines: [to add].

## Reviewer #5

### Comment 1: Add computational workflow schematic

We added a new workflow schematic. It shows synthetic range definition, dataset generation, model fitting, internal auditing, literature-derived stress testing, intended post-characterization use, and the need for future prospective validation.

Changes made: New workflow figure and caption. Lines: [to add].

### Comment 2: Report feature units consistently

We added units or scales for all predictor variables. DAR_Mean is reported as mol drug per mol antibody, DAR_Std in DAR units, DAR_CV as a unitless relative dispersion measure, Latency_to_Clinic_yrs in years, and the remaining manufacturability/developability scores as dimensionless normalized 0-1 scores.

Changes made: Methods; predictor-variable table. Lines: [to add].

### Comment 3: Feature perturbation / sensitivity analysis

We added a feature perturbation sensitivity script and incorporated the synthetic perturbation/noise-stress concept into the model-quality audit. This analysis is framed as internal stress testing of the synthetic benchmark, not as external validation.

Changes made: Methods/Results model-quality audit; Table II; repository script. Lines: [to add].

### Comment 4: Table defining every predictor variable

We added a predictor-variable table defining each feature, unit/scale, synthetic representation, practical pharmaceutical meaning, expected availability in a real ADC workflow, and manuscript interpretation.

Changes made: Predictor-variable table; Methods. Lines: [to add].

### Comment 5: Transfer learning/federated learning future direction

We added a short future-work paragraph noting that transfer learning or privacy-preserving federated learning could eventually help incorporate confidential industrial ADC datasets. We also state that such approaches would require harmonized feature definitions, locked endpoints, batch grouping, independent test cohorts, and prospective validation.

Changes made: Discussion future work. Lines: [to add].

### Additional practical-positioning concern

We revised the manuscript to clarify that the current tool uses variables that are generally available only after early conjugation and characterization. It is therefore positioned as a proof-of-concept decision-support and documentation aid during early process optimization, not as a validated pre-experimental platform-selection model.

Changes made: Abstract; Introduction; Methods; Discussion; Conclusion. Lines: [to add].

## Closing

We believe these revisions make the manuscript more transparent and better aligned with the current evidence. The revised manuscript now emphasizes the exploratory nature of the model, reports internal uncertainty more clearly, and avoids presenting literature-derived concordance as external validation.
