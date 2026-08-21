"""Feature perturbation sensitivity analysis for the ADC platform classifier.

This script supports the second-round AAPSJ revision. It trains the Random Forest
on the synthetic dataset, perturbs one numeric feature at a time, and records how
often the predicted platform changes and how much the predicted probability for
the original class changes.

The analysis is intentionally framed as synthetic stress testing, not external
validation.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "adc_conjugation_synthetic_advanced.csv"
OUT_DIR = ROOT / "reports" / "feature_perturbation_sensitivity" / "tables"

NUMERIC_FEATURES_9 = [
    "DAR_Mean",
    "DAR_Std",
    "DAR_CV",
    "Homogeneity",
    "Stability_Score",
    "Expression_Ease",
    "Cost_Index",
    "Scalability",
    "Latency_to_Clinic_yrs",
]

# Seven-feature set used in the revised sensitivity audit after removing the two
# most redundant variables discussed in the manuscript.
NUMERIC_FEATURES_7 = [
    "DAR_Mean",
    "DAR_CV",
    "Homogeneity",
    "Stability_Score",
    "Expression_Ease",
    "Scalability",
    "Latency_to_Clinic_yrs",
]

PERTURBATIONS = [-0.20, -0.10, 0.10, 0.20]
RANDOM_STATE = 42


def build_model() -> Pipeline:
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "rf",
                RandomForestClassifier(
                    n_estimators=500,
                    random_state=RANDOM_STATE,
                    class_weight="balanced_subsample",
                ),
            ),
        ]
    )


def perturb_feature_values(
    X: pd.DataFrame, feature: str, fraction: float, training_min: float, training_max: float
) -> pd.DataFrame:
    Xp = X.copy()
    Xp[feature] = Xp[feature] * (1.0 + fraction)
    Xp[feature] = Xp[feature].clip(lower=training_min, upper=training_max)
    return Xp


def run_analysis(feature_set_name: str, features: list[str], df: pd.DataFrame) -> pd.DataFrame:
    X = df[features].copy()
    y = df["Platform"].copy()

    model = build_model()
    model.fit(X, y)

    baseline_pred = model.predict(X)
    baseline_proba = model.predict_proba(X)
    class_index = {label: idx for idx, label in enumerate(model.classes_)}
    baseline_chosen_proba = np.array(
        [baseline_proba[i, class_index[pred]] for i, pred in enumerate(baseline_pred)]
    )

    rows = []
    for feature in features:
        training_min = float(X[feature].min())
        training_max = float(X[feature].max())
        for fraction in PERTURBATIONS:
            Xp = perturb_feature_values(X, feature, fraction, training_min, training_max)
            perturbed_pred = model.predict(Xp)
            perturbed_proba = model.predict_proba(Xp)
            perturbed_baseline_class_proba = np.array(
                [perturbed_proba[i, class_index[pred]] for i, pred in enumerate(baseline_pred)]
            )
            changed = perturbed_pred != baseline_pred
            rows.append(
                {
                    "feature_set": feature_set_name,
                    "feature": feature,
                    "perturbation_fraction": fraction,
                    "records_changed": int(changed.sum()),
                    "records_total": int(len(X)),
                    "prediction_change_rate": float(changed.mean()),
                    "mean_abs_probability_shift_for_baseline_class": float(
                        np.mean(np.abs(perturbed_baseline_class_proba - baseline_chosen_proba))
                    ),
                    "max_abs_probability_shift_for_baseline_class": float(
                        np.max(np.abs(perturbed_baseline_class_proba - baseline_chosen_proba))
                    ),
                }
            )
    return pd.DataFrame(rows)


def run_cv_baseline(features: list[str], df: pd.DataFrame) -> pd.DataFrame:
    X = df[features].copy()
    y = df["Platform"].copy()
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
    model = build_model()
    pred = cross_val_predict(model, X, y, cv=cv)
    return pd.DataFrame({"true_platform": y, "cv_predicted_platform": pred})


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA_PATH)

    full = run_analysis("9-feature", NUMERIC_FEATURES_9, df)
    reduced = run_analysis("7-feature", NUMERIC_FEATURES_7, df)
    combined = pd.concat([full, reduced], ignore_index=True)
    combined.to_csv(OUT_DIR / "feature_perturbation_sensitivity.csv", index=False)

    summary = (
        combined.groupby(["feature_set", "feature"], as_index=False)
        .agg(
            max_prediction_change_rate=("prediction_change_rate", "max"),
            mean_prediction_change_rate=("prediction_change_rate", "mean"),
            max_probability_shift=("max_abs_probability_shift_for_baseline_class", "max"),
            mean_probability_shift=("mean_abs_probability_shift_for_baseline_class", "mean"),
        )
        .sort_values(["feature_set", "max_prediction_change_rate", "max_probability_shift"], ascending=[True, False, False])
    )
    summary.to_csv(OUT_DIR / "feature_perturbation_sensitivity_summary.csv", index=False)

    cv_baseline = run_cv_baseline(NUMERIC_FEATURES_7, df)
    cv_baseline.to_csv(OUT_DIR / "seven_feature_cv_predictions.csv", index=False)

    print("Wrote:")
    print(OUT_DIR / "feature_perturbation_sensitivity.csv")
    print(OUT_DIR / "feature_perturbation_sensitivity_summary.csv")
    print(OUT_DIR / "seven_feature_cv_predictions.csv")


if __name__ == "__main__":
    main()
