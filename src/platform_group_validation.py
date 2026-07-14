from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, matthews_corrcoef
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adc_conjugation_synthetic_advanced.csv"
OUT = ROOT / "reports" / "platform_group_validation"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"
for folder in (TABLES, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

SEED = 42
FEATURES = [
    "DAR_Mean",
    "DAR_CV",
    "Homogeneity",
    "Stability_Score",
    "Expression_Ease",
    "Scalability",
    "Latency_to_Clinic_yrs",
]


def pipeline(estimator):
    prep = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), FEATURES)
    ])
    return Pipeline([("preprocessing", prep), ("classifier", estimator)])


MODELS = {
    "Logistic regression": pipeline(LogisticRegression(
        max_iter=3000, class_weight="balanced", random_state=SEED
    )),
    "Random Forest": pipeline(RandomForestClassifier(
        n_estimators=1000, class_weight="balanced", random_state=SEED, n_jobs=1
    )),
    "Extra Trees": pipeline(ExtraTreesClassifier(
        n_estimators=1000, class_weight="balanced", random_state=SEED, n_jobs=1
    )),
}


def main():
    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y = df["Technology_Category"]
    groups = df["Platform"]
    logo = LeaveOneGroupOut()
    classes = sorted(y.unique())
    rows = []
    prediction_rows = []
    matrices = {name: np.zeros((len(classes), len(classes)), dtype=int) for name in MODELS}

    for fold, (train_idx, test_idx) in enumerate(logo.split(X, y, groups)):
        held_out = groups.iloc[test_idx].iloc[0]
        held_category = y.iloc[test_idx].iloc[0]
        train_categories = sorted(y.iloc[train_idx].unique())
        category_absent = held_category not in train_categories
        for model_name, template in MODELS.items():
            model = clone(template)
            model.fit(X.iloc[train_idx], y.iloc[train_idx])
            pred = model.predict(X.iloc[test_idx])
            matrices[model_name] += confusion_matrix(y.iloc[test_idx], pred, labels=classes)
            rows.append({
                "fold": fold,
                "held_out_platform": held_out,
                "held_out_category": held_category,
                "n_train": len(train_idx),
                "n_test": len(test_idx),
                "training_categories": "; ".join(train_categories),
                "held_out_category_absent_from_training": category_absent,
                "model": model_name,
                "accuracy": accuracy_score(y.iloc[test_idx], pred),
                "macro_f1_observed_labels": f1_score(y.iloc[test_idx], pred, average="macro"),
                "mcc": matthews_corrcoef(y.iloc[test_idx], pred),
                "most_common_prediction": pd.Series(pred).mode().iloc[0],
                "n_unique_predictions": pd.Series(pred).nunique(),
            })
            for idx, predicted in zip(test_idx, pred):
                prediction_rows.append({
                    "model": model_name,
                    "held_out_platform": held_out,
                    "true_category": y.iloc[idx],
                    "predicted_category": predicted,
                    "correct": predicted == y.iloc[idx],
                    "category_absent_from_training": category_absent,
                })

    results = pd.DataFrame(rows)
    predictions = pd.DataFrame(prediction_rows)
    results.to_csv(TABLES / "leave_one_platform_out_results.csv", index=False)
    predictions.to_csv(TABLES / "leave_one_platform_out_predictions.csv", index=False)

    representable = results[~results["held_out_category_absent_from_training"]]
    summary = results.groupby("model").agg(
        all_fold_accuracy=("accuracy", "mean"),
        all_fold_accuracy_sd=("accuracy", "std"),
        folds=("fold", "count"),
    ).reset_index()
    represented_summary = representable.groupby("model").agg(
        representable_fold_accuracy=("accuracy", "mean"),
        representable_fold_accuracy_sd=("accuracy", "std"),
        representable_folds=("fold", "count"),
    ).reset_index()
    summary = summary.merge(represented_summary, on="model", how="left")
    summary.to_csv(TABLES / "leave_one_platform_out_summary.csv", index=False)

    for model_name, matrix in matrices.items():
        safe = model_name.lower().replace(" ", "_")
        pd.DataFrame(matrix, index=classes, columns=classes).to_csv(
            TABLES / f"grouped_confusion_{safe}.csv"
        )

    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=results,
        x="accuracy",
        y="held_out_platform",
        hue="model",
        ax=ax,
    )
    ax.set_xlim(0, 1)
    ax.set_xlabel("Accuracy on all eight records from held-out platform")
    ax.set_ylabel("")
    ax.set_title("Leave-one-platform-out category generalization")
    fig.tight_layout()
    fig.savefig(FIGURES / "leave_one_platform_out_accuracy.png", dpi=300)
    plt.close(fig)

    singleton = (
        df[["Platform", "Technology_Category"]]
        .drop_duplicates()
        .groupby("Technology_Category")["Platform"]
        .nunique()
        .rename("named_platforms")
        .reset_index()
    )
    singleton.to_csv(TABLES / "named_platforms_per_category.csv", index=False)

    report = {
        "target": "Technology_Category",
        "group": "Platform",
        "features": FEATURES,
        "named_platforms_per_category": singleton.to_dict(orient="records"),
        "model_summary": summary.to_dict(orient="records"),
        "fold_results": results.to_dict(orient="records"),
        "structural_limitation": (
            "The Random category contains only one named platform (Lysine-Based). "
            "When Lysine-Based is held out, Random is absent from training, so successful prediction is impossible. "
            "The all-fold average is therefore descriptive, not a fair estimate of unseen-platform generalization."
        ),
        "required_next_step": (
            "Add at least two independently sourced named platforms per technology category and group all records from each platform/program together."
        ),
    }
    (OUT / "platform_group_validation_summary.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
