# Python-based ML model for ADC conjugation-platform selection

This repository contains an exploratory, proof-of-concept Python workflow for antibody-drug conjugate (ADC) conjugation-platform classification. The project was developed to study whether developability-oriented features could support a CMC-layer platform-selection question that is not directly addressed by most published ADC activity-prediction models.

Important limitation: the training dataset is synthetic and class-conditioned. The reported model performance describes behavior on a controlled benchmark, not validated performance for real ADC development programs. The literature-derived 20-ADC assessment is provided as a face-validity and transportability stress test, not external validation.

## What this repository includes

- Recovery of the original 48-record synthetic ADC conjugation-platform dataset.
- Exploratory data analysis notebooks.
- Model benchmarking notebooks and scripts.
- Additional reviewer-revision analyses:
  - repeated and nested cross-validation;
  - metrics beyond accuracy, including macro-F1, MCC, kappa, log loss, and Brier score;
  - hold-out split seed sensitivity;
  - redundant-feature ablation;
  - leave-one-named-platform-out testing;
  - literature-derived 20-ADC stress testing;
  - feature-range / applicability-domain warnings.
- Demonstration Gradio interface and serialized models for reproducing the synthetic benchmark workflow.

The code is intended for reproducibility, education, and methods development. It should not be used to choose an ADC conjugation platform for an experimental or industrial program without independent experimental validation.

## Repository structure

```text
data/
  adc_conjugation_synthetic_advanced.csv     Synthetic 48-record benchmark dataset
  literature_validation_20.csv               Literature-derived 20-ADC stress-test table
  synthetic_data_generator.ipynb             Original synthetic-data generator notebook

notebooks/
  01_data_exploration.ipynb                  Exploratory analysis
  02_model_selection.ipynb                   Original model training workflow
  03_platform_recommender.ipynb              Demonstration interface workflow

src/
  revision_analysis.py                       Feature ablation and literature-compatibility audit
  rigorous_model_audit.py                    Repeated/nested CV and model-quality audit
  metric_quality_audit.py                    Metrics beyond accuracy and seed sensitivity
  platform_group_validation.py               Leave-one-named-platform-out testing
  validation_20_audit.py                     20-ADC literature stress-test analysis

models/
  Serialized models used for reproducibility of the benchmark/demo workflow

reports/
  Tables, figures, JSON summaries, and revised manuscript-support analyses
```

## Installation

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/camontefusco/Python-based-ML-model-for-ADC-Conjugation-Platform-Selection.git
cd Python-based-ML-model-for-ADC-Conjugation-Platform-Selection
python -m venv .venv
source .venv/bin/activate
pip install -r requirements
```

## Reproducing the revision analyses

Run the scripts from the repository root:

```bash
python src/rigorous_model_audit.py
python src/metric_quality_audit.py
python src/platform_group_validation.py
python src/validation_20_audit.py
python src/revision_analysis.py
```

The scripts write CSV tables, figures, and JSON summaries under `reports/`.

## Data

The synthetic dataset contains 48 records: six named conjugation-platform archetypes with eight records per platform. Features include DAR summary metrics, homogeneity, stability, expression ease, scalability, and related development descriptors.

The dataset was designed as a transparent benchmark for workflow development. It is not an industrial ADC dataset and does not capture all sources of experimental variability, assay noise, project-level dependence, failed programs, process history, payload effects, or organization-specific CMC constraints.

The 20-ADC literature table is incomplete by design because public sources do not consistently report all features required by the synthetic model. It is therefore used only for constrained stress tests.

## Main revised results

In one 10-record hold-out split, the Random Forest achieved perfect accuracy. Broader testing was more cautious:

- repeated cross-validation accuracy for the revised audit model was approximately 0.83;
- macro-F1 was approximately 0.81;
- leave-one-named-platform-out testing showed weak transfer between platform families;
- removal of constructed redundant variables did not materially change internal performance;
- the 20-ADC literature-derived assessment gave 4/20 agreement for a strict two-feature check and 16/20 agreement for a partly harmonized five-feature check.

These results support the workflow as a reproducible scaffold, not as a validated decision-support tool.

## Models

Serialized models are included only to reproduce the synthetic benchmark and demonstration interface. Model scores should be treated as uncalibrated. They are not probabilities suitable for ADC development decisions.

## Citation

If you use this repository, please cite the GitHub repository and, once available, the associated manuscript.

```text
Montefusco-Pereira CA. Python-based ML model for ADC conjugation-platform selection. GitHub.
https://github.com/camontefusco/Python-based-ML-model-for-ADC-Conjugation-Platform-Selection
```

## Contact

Carlos Montefusco-Pereira  
GitHub: https://github.com/camontefusco

