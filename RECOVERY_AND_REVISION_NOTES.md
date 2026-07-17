# ADC conjugation platform project recovery

## Recovered sources

The original GitHub repository stored project components on separate branches rather than in directories on `main`:

- `data`: exact 48-row synthetic dataset and generator notebook
- `notebooks`: exploration, model-selection, and recommender notebooks
- `models`: original serialized Random Forest pipeline
- `reports`: original PDF reports
- `main`: README, banner, and requirements file

These branch contents have been consolidated into this conventional working tree without altering the remote branches.

## Exact synthetic dataset

`data/adc_conjugation_synthetic_advanced.csv` is the original dataset recovered from the GitHub `data` branch. It contains 48 records, 14 columns, six platforms, and eight records per platform. It was not reconstructed from figures or regenerated approximately.

## Reviewer-revision analysis

`src/revision_analysis.py` adds analyses requested during major revision:

- 4-fold repeated stratified cross-validation with 10 repeats;
- accuracy, balanced accuracy, and macro-F1 distributions;
- empirical 95% intervals across repeated folds;
- Wilson 95% confidence interval for the 10-record hold-out result;
- label-permutation testing;
- sensitivity analyses after removing `Cost_Index`, then both `Cost_Index` and `DAR_Std`;
- a category-level Random Forest using only features shared by the synthetic and literature datasets;
- direct trained-model application to the 20 literature-curated ADCs;
- feature-range audit and explicit out-of-domain flags;
- export of models, tables, figures, and machine-readable JSON results.

## Corrected interpretation

The original 19/20 result came from the validation notebook's rule-based fallback because the serialized model path was unavailable. It was not external validation of the trained Random Forest.

The new validation-compatible Random Forest predicts 16/20 literature records correctly (80%; Wilson 95% CI 58.4%-91.9%). Every literature record has at least one shared feature outside the synthetic training range. The result is therefore a preliminary model-compatibility or transportability stress test, not evidence of generalizable external performance.

Repeated-CV accuracy is 0.846 for the nine-feature model, 0.829 after removing `Cost_Index`, and 0.833 after also removing `DAR_Std`. This supports removal of the constructed collinear feature without a material loss of internal discrimination, while still acknowledging that the labels and feature distributions were synthetically constructed.
