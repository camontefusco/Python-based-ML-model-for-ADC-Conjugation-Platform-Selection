# Second-round AAPSJ review work area

Branch: `second-round-reviewer-revision-2026-08`

This folder collects the scientific decisions and replacement materials for the second major revision of the AAPSJ manuscript.

## Files

- `manuscript_change_map.md` - maps each reviewer concern to required manuscript edits.
- `Table_II_replacement.csv` - clean replacement for the model-quality audit table.
- `Table_III_replacement.csv` - clean replacement for the 20-ADC literature stress-test table, with the withdrawn 19/20 rule-based result separated from current model results.
- `predictor_variable_definitions.csv` - predictor definitions, units/scales, practical meaning, and availability in the ADC workflow.
- `workflow_schematic_spec.md` - design specification for the new computational workflow schematic requested by Reviewer #5.
- `keyword_revision.txt` - revised keyword recommendation.
- `response_letter_skeleton.md` - response-letter structure to fill only after marked manuscript edits and line numbers are available.

## Main scientific repositioning

The revised manuscript should describe the framework as a proof-of-concept classifier and decision-support aid after early conjugation/characterization data are available. It should not be presented as a validated prospective platform-selection model before experimental work.

## Analyses already available in the repo

- Repeated CV and model benchmark: `reports/rigorous_model_audit/tables/repeated_cv_model_benchmark.csv`
- Nested CV: `reports/rigorous_model_audit/tables/nested_cv_random_forest.csv`
- Hold-out seed sensitivity: `reports/metric_quality_audit/tables/random_forest_holdout_seed_sensitivity.csv`
- Leave-one-platform-out validation: `reports/platform_group_validation/tables/leave_one_platform_out_results.csv`
- Redundant-feature ablation: `reports/revision_analysis/tables/repeated_cv_feature_sensitivity.csv`
- Noise stress test: `reports/rigorous_model_audit/tables/random_forest_noise_stress_test.csv`
- Revised 20-ADC audit: `reports/validation_20_audit/tables/validation_20_model_summary.csv`

## New analysis to run when local execution is available

Run:

```bash
python src/feature_perturbation_sensitivity.py
```

Expected outputs:

- `reports/feature_perturbation_sensitivity/tables/feature_perturbation_sensitivity.csv`
- `reports/feature_perturbation_sensitivity/tables/feature_perturbation_sensitivity_summary.csv`
- `reports/feature_perturbation_sensitivity/tables/seven_feature_cv_predictions.csv`

