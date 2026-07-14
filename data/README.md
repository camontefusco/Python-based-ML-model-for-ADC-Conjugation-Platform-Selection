# Data

This folder contains the datasets used by the exploratory ADC conjugation-platform workflow.

## Files

- `adc_conjugation_synthetic_advanced.csv`  
  Original recovered 48-record synthetic benchmark dataset. It contains six named conjugation-platform archetypes, with eight records per platform.

- `literature_validation_20.csv`  
  Literature-derived table of 20 ADC programs used for constrained face-validity and transportability stress tests.

- `synthetic_data_generator.ipynb`  
  Notebook used to generate the synthetic benchmark dataset.

## Synthetic dataset columns

The synthetic dataset includes:

- `Technology_Category`
- `Platform`
- `Vendor`
- `DAR_Mean`
- `DAR_Std`
- `DAR_CV`
- `Homogeneity`
- `Stability_Score`
- `Expression_Ease`
- `Cost_Index`
- `CMC_Risk`
- `Scalability`
- `Latency_to_Clinic_yrs`
- `Approved_Usage`

## Interpretation

The synthetic dataset was created to support workflow development and controlled model-quality audits. It should not be interpreted as a real industrial CMC dataset. Platform-specific ranges were intentionally class-conditioned, so internal model performance reflects separation built into the simulation.

The 20-ADC literature table is not a locked external validation cohort. Public sources do not provide complete, consistently measured feature vectors for all records, so the table is used only for stress testing and failure-mode analysis.

