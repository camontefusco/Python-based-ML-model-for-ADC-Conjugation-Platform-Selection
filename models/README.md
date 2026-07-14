# Models

This folder contains serialized models used to reproduce the synthetic benchmark analyses and the demonstration interface.

## Important limitation

These models were trained on a small synthetic, class-conditioned dataset. They are not validated for real ADC platform-selection decisions, and their output scores should not be treated as calibrated probabilities.

## Files

- `rf_adc_pipeline.pkl`  
  Original Random Forest pipeline recovered from the initial repository.

- `rf_platform_full_holdout.joblib`  
  Random Forest model used for the original full-platform hold-out workflow.

- `rf_platform_reduced.joblib`  
  Reduced-feature Random Forest model used in revision sensitivity analyses.

- `rf_category_external_compatible.joblib`  
  Category-level model using features compatible with the constrained 20-ADC literature stress test.

Use these files for reproducibility only. For future experimental work, models should be retrained from locked scripts on independent, consistently measured ADC program records.

