# Second-round manuscript change map

This file maps the new reviewer comments to the manuscript changes that should be made before drafting the point-by-point response letter.

## Global positioning change

Revise Abstract, end of Introduction, Methods workflow, Results validation section, Discussion, and Conclusion to state that the framework is a proof-of-concept post-characterization classifier and decision-support workflow. It should not be described as a validated pre-conjugation platform selector, because several required inputs (DAR distribution, DAR_CV, Homogeneity, Stability_Score) are obtained only after early conjugation and characterization.

Suggested plain wording: "The current framework is best interpreted as a proof-of-concept classifier and decision-support aid after early conjugation/characterization data are available. It does not yet establish prospective platform selection before experimental work."

## Reviewer #3

- Synthetic dataset representativeness: expand Methods with platform-specific range construction, synthetic assignment process, and limitations of class-conditioned separation. Add reference to Supplementary Table S1 / predictor definition table.
- Hold-out 1.00 accuracy: revise Results to present the 10/10 result with Wilson CI and immediately report repeated CV, nested CV, seed sensitivity, and leave-one-platform-out stress testing from Table II.
- 95% concordance confusion: remove any Abstract/Conclusion wording that implies the threshold-rule concordance validates the Random Forest. Table III should not include the withdrawn 19/20 result as an active model result.
- Six-class versus three-category literature check: explain that six-class prediction was the internal synthetic training task, whereas literature reporting supports only broader technology categories; therefore the 20-ADC assessment is a category-level stress test.
- Collinearity: identify Expression_Ease and Cost_Index as nearly collinear; state that Cost_Index was removed in sensitivity analysis and that feature importance/SHAP are interpreted cautiously.
- Graphical abstract: ensure feature list matches Methods or use wording "representative developability/manufacturability features" if not listing all nine.

## Reviewer #4

- Table II: replace current table with clean model-quality audit table (`Table_II_replacement.csv`).
- Table III: remove or clearly separate the withdrawn 19/20 threshold-rule result. Preferred: remove from table and describe as superseded in text.
- Keywords: replace "Drug Development" with more specific ADC/CMC/model-validation keywords.

## Reviewer #5

- Workflow schematic: add a new computational workflow figure showing synthetic data generation -> preprocessing -> model training -> internal audit -> literature stress test -> demo decision support -> future prospective validation.
- Units: add units/scales for all predictor variables in Methods and table captions.
- Feature perturbation: use existing noise-stress analysis as synthetic perturbation evidence; if local execution becomes available, add feature-level perturbation by changing one feature at a time and recording prediction changes/probability shifts.
- Predictor definitions: add main or supplementary table from `predictor_variable_definitions.csv`.
- Transfer/federated learning: add a short Discussion paragraph as a future direction for confidential industrial datasets, with a warning that it requires harmonized feature definitions and locked endpoints.
- Practical aim: clarify that the tool supports early process optimization/documentation after initial conjugation data, not de novo selection before experiments.

## Response letter sequencing

Draft the response letter only after the marked manuscript edits are made. Each response should cite the changed section and line numbers from the final marked manuscript.
