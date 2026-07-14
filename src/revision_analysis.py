from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import binomtest
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
)
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_validate,
    permutation_test_score,
    train_test_split,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "reports" / "revision_analysis"
FIG = OUT / "figures"
CSV = OUT / "tables"
MODELS = ROOT / "models"
for folder in (FIG, CSV, MODELS):
    folder.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
FULL_FEATURES = [
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
REDUCED_FEATURES = [feature for feature in FULL_FEATURES if feature != "Cost_Index"]
PARSIMONIOUS_FEATURES = [
    feature for feature in REDUCED_FEATURES if feature != "DAR_Std"
]
EXTERNAL_FEATURES = [
    "DAR_Mean",
    "DAR_CV",
    "Stability_Score",
    "Homogeneity",
    "Scalability",
]


def make_pipeline(features: list[str], n_estimators: int = 200) -> Pipeline:
    preprocessing = ColumnTransformer(
        [
            (
                "numeric",
                Pipeline(
                    [
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ]
                ),
                features,
            )
        ],
        remainder="drop",
    )
    return Pipeline(
        [
            ("preprocessing", preprocessing),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=n_estimators,
                    random_state=RANDOM_STATE,
                    class_weight="balanced",
                    min_samples_leaf=1,
                    n_jobs=1,
                ),
            ),
        ]
    )


def score_interval(values: np.ndarray) -> tuple[float, float]:
    return tuple(np.quantile(values, [0.025, 0.975]).tolist())


def repeated_cv_sensitivity(df: pd.DataFrame) -> pd.DataFrame:
    target = df["Platform"]
    repeated_cv = RepeatedStratifiedKFold(
        n_splits=4,
        n_repeats=10,
        random_state=RANDOM_STATE,
    )
    rows = []
    feature_sets = {
        "Full (9 features)": FULL_FEATURES,
        "Cost_Index removed (8 features)": REDUCED_FEATURES,
        "Cost_Index and DAR_Std removed (7 features)": PARSIMONIOUS_FEATURES,
    }
    for label, features in feature_sets.items():
        result = cross_validate(
            make_pipeline(features),
            df[features],
            target,
            cv=repeated_cv,
            scoring={
                "accuracy": "accuracy",
                "balanced_accuracy": "balanced_accuracy",
                "macro_f1": "f1_macro",
            },
            n_jobs=1,
        )
        row = {"Feature set": label, "Number of features": len(features)}
        for metric in ("accuracy", "balanced_accuracy", "macro_f1"):
            values = result[f"test_{metric}"]
            low, high = score_interval(values)
            row[f"{metric}_mean"] = values.mean()
            row[f"{metric}_sd"] = values.std(ddof=1)
            row[f"{metric}_empirical_95_low"] = low
            row[f"{metric}_empirical_95_high"] = high
        rows.append(row)
    return pd.DataFrame(rows)


def holdout_analysis(df: pd.DataFrame) -> tuple[pd.DataFrame, Pipeline]:
    X_train, X_test, y_train, y_test = train_test_split(
        df[FULL_FEATURES],
        df["Platform"],
        test_size=0.20,
        random_state=RANDOM_STATE,
        stratify=df["Platform"],
    )
    model = make_pipeline(FULL_FEATURES)
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, pred)
    interval = binomtest(int((pred == y_test).sum()), len(y_test)).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    summary = pd.DataFrame(
        [
            {
                "n_test": len(y_test),
                "correct": int((pred == y_test).sum()),
                "accuracy": accuracy,
                "wilson_95_low": interval.low,
                "wilson_95_high": interval.high,
                "macro_f1": f1_score(y_test, pred, average="macro"),
                "balanced_accuracy": balanced_accuracy_score(y_test, pred),
            }
        ]
    )
    labels = sorted(df["Platform"].unique())
    cm = pd.DataFrame(
        confusion_matrix(y_test, pred, labels=labels),
        index=labels,
        columns=labels,
    )
    cm.to_csv(CSV / "holdout_confusion_matrix.csv")
    return summary, model


def permutation_analysis(df: pd.DataFrame) -> pd.DataFrame:
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=RANDOM_STATE)
    score, permutation_scores, p_value = permutation_test_score(
        make_pipeline(PARSIMONIOUS_FEATURES, n_estimators=100),
        df[PARSIMONIOUS_FEATURES],
        df["Platform"],
        scoring="accuracy",
        cv=cv,
        n_permutations=100,
        n_jobs=1,
        random_state=RANDOM_STATE,
    )
    pd.DataFrame({"permuted_accuracy": permutation_scores}).to_csv(
        CSV / "permutation_scores.csv",
        index=False,
    )
    return pd.DataFrame(
        [{"observed_cv_accuracy": score, "permutation_p_value": p_value}]
    )


def prepare_external_validation(
    training: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    validation = pd.read_csv(DATA / "literature_validation_20.csv")
    external = pd.DataFrame(
        {
            "DAR_Mean": validation["dar_mean"],
            "DAR_CV": validation["dar_cv"],
            "Stability_Score": validation["stability_score"] / 5.0,
            "Homogeneity": validation["homogeneity_score"] / 5.0,
            "Scalability": validation["manufacturability"] / 5.0,
        }
    )
    range_rows = []
    outside_any = np.zeros(len(external), dtype=bool)
    for feature in EXTERNAL_FEATURES:
        low = training[feature].min()
        high = training[feature].max()
        outside = (external[feature] < low) | (external[feature] > high)
        outside_any |= outside.to_numpy()
        range_rows.append(
            {
                "feature": feature,
                "training_min": low,
                "training_max": high,
                "external_min": external[feature].min(),
                "external_max": external[feature].max(),
                "external_records_outside_range": int(outside.sum()),
            }
        )
    validation["outside_training_range"] = outside_any
    return validation.join(external.add_prefix("model_")), pd.DataFrame(range_rows)


def external_model_analysis(training: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    validation, ranges = prepare_external_validation(training)
    model = make_pipeline(EXTERNAL_FEATURES, n_estimators=500)
    model.fit(training[EXTERNAL_FEATURES], training["Technology_Category"])
    external_X = validation[[f"model_{feature}" for feature in EXTERNAL_FEATURES]].copy()
    external_X.columns = EXTERNAL_FEATURES
    pred = model.predict(external_X)
    probabilities = model.predict_proba(external_X)
    validation["rf_predicted_category"] = pred
    validation["rf_max_probability"] = probabilities.max(axis=1)
    validation["rf_concordant"] = pred == validation["platform_category"]
    validation.to_csv(CSV / "external_rf_predictions.csv", index=False)
    ranges.to_csv(CSV / "external_feature_range_audit.csv", index=False)

    correct = int(validation["rf_concordant"].sum())
    n = len(validation)
    interval = binomtest(correct, n).proportion_ci(
        confidence_level=0.95,
        method="wilson",
    )
    overall = {
        "Platform category": "Overall",
        "Correct": correct,
        "Total": n,
        "Concordance": correct / n,
        "Wilson 95% low": interval.low,
        "Wilson 95% high": interval.high,
    }
    rows = [overall]
    for category, subset in validation.groupby("platform_category", sort=True):
        category_correct = int(subset["rf_concordant"].sum())
        category_n = len(subset)
        category_interval = binomtest(category_correct, category_n).proportion_ci(
            confidence_level=0.95,
            method="wilson",
        )
        rows.append(
            {
                "Platform category": category,
                "Correct": category_correct,
                "Total": category_n,
                "Concordance": category_correct / category_n,
                "Wilson 95% low": category_interval.low,
                "Wilson 95% high": category_interval.high,
            }
        )
    summary = pd.DataFrame(rows)
    summary.to_csv(CSV / "external_rf_concordance_summary.csv", index=False)
    joblib.dump(model, MODELS / "rf_category_external_compatible.joblib")
    return validation, summary


def correlations_and_importance(training: pd.DataFrame) -> pd.DataFrame:
    corr = training[FULL_FEATURES].corr(method="pearson")
    corr.to_csv(CSV / "feature_correlations.csv")
    model = make_pipeline(PARSIMONIOUS_FEATURES, n_estimators=500)
    model.fit(training[PARSIMONIOUS_FEATURES], training["Platform"])
    importance = pd.DataFrame(
        {
            "feature": PARSIMONIOUS_FEATURES,
            "mdi_importance": model.named_steps["classifier"].feature_importances_,
        }
    ).sort_values("mdi_importance", ascending=False)
    importance.to_csv(CSV / "reduced_model_mdi_importance.csv", index=False)
    joblib.dump(model, MODELS / "rf_platform_reduced.joblib")
    return importance


def make_figures(
    sensitivity: pd.DataFrame,
    validation: pd.DataFrame,
    external_summary: pd.DataFrame,
) -> None:
    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    y = np.arange(len(sensitivity))
    means = sensitivity["accuracy_mean"].to_numpy()
    low = sensitivity["accuracy_empirical_95_low"].to_numpy()
    high = sensitivity["accuracy_empirical_95_high"].to_numpy()
    ax.errorbar(means, y, xerr=[means - low, high - means], fmt="o", capsize=5)
    ax.set_yticks(y, sensitivity["Feature set"])
    ax.set_xlim(0, 1.03)
    ax.set_xlabel("Repeated-CV accuracy (mean and empirical 95% interval)")
    ax.set_title("Random Forest sensitivity to redundant-feature removal")
    fig.tight_layout()
    fig.savefig(FIG / "feature_removal_sensitivity.png", dpi=300)
    plt.close(fig)

    plot_data = external_summary[external_summary["Platform category"] != "Overall"]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.barplot(data=plot_data, x="Concordance", y="Platform category", ax=ax)
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("Concordance")
    ax.set_ylabel("")
    ax.set_title("Trained category-level Random Forest: literature-set concordance")
    fig.tight_layout()
    fig.savefig(FIG / "external_rf_concordance.png", dpi=300)
    plt.close(fig)

    discordant = validation.loc[
        ~validation["rf_concordant"],
        ["name", "platform_category", "rf_predicted_category", "rf_max_probability"],
    ]
    discordant.to_csv(CSV / "external_rf_discordant_cases.csv", index=False)


def main() -> None:
    training = pd.read_csv(DATA / "adc_conjugation_synthetic_advanced.csv")
    assert len(training) == 48
    assert training["Platform"].value_counts().eq(8).all()

    sensitivity = repeated_cv_sensitivity(training)
    sensitivity.to_csv(CSV / "repeated_cv_feature_sensitivity.csv", index=False)

    holdout, holdout_model = holdout_analysis(training)
    holdout.to_csv(CSV / "holdout_uncertainty.csv", index=False)
    joblib.dump(holdout_model, MODELS / "rf_platform_full_holdout.joblib")

    permutation = permutation_analysis(training)
    permutation.to_csv(CSV / "permutation_test_summary.csv", index=False)

    importance = correlations_and_importance(training)
    validation, external_summary = external_model_analysis(training)
    make_figures(sensitivity, validation, external_summary)

    report = {
        "training_records": len(training),
        "platforms": int(training["Platform"].nunique()),
        "holdout": holdout.iloc[0].to_dict(),
        "permutation": permutation.iloc[0].to_dict(),
        "repeated_cv": sensitivity.to_dict(orient="records"),
        "external_validation": external_summary.to_dict(orient="records"),
        "external_records_outside_any_training_range": int(
            validation["outside_training_range"].sum()
        ),
        "reduced_model_importance": importance.to_dict(orient="records"),
    }
    (OUT / "analysis_summary.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
