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
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    cohen_kappa_score,
    confusion_matrix,
    f1_score,
    log_loss,
    matthews_corrcoef,
    precision_recall_fscore_support,
    roc_auc_score,
    top_k_accuracy_score,
)
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelBinarizer, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adc_conjugation_synthetic_advanced.csv"
OUT = ROOT / "reports" / "metric_quality_audit"
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


def make_pipeline(classifier, features=FEATURES):
    preprocessing = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), features)
    ])
    return Pipeline([("preprocessing", preprocessing), ("classifier", classifier)])


MODELS = {
    "Logistic regression": make_pipeline(LogisticRegression(max_iter=3000, random_state=SEED)),
    "Linear SVM": make_pipeline(SVC(kernel="linear", C=1.0, probability=True, random_state=SEED)),
    "Random Forest": make_pipeline(RandomForestClassifier(
        n_estimators=300, class_weight="balanced", random_state=SEED, n_jobs=1
    )),
    "Extra Trees": make_pipeline(ExtraTreesClassifier(
        n_estimators=300, class_weight="balanced", random_state=SEED, n_jobs=1
    )),
}


def multiclass_brier(y_true, probabilities, classes):
    one_hot = LabelBinarizer().fit(classes).transform(y_true)
    return float(np.mean(np.sum((probabilities - one_hot) ** 2, axis=1)))


def top_label_ece(y_true, pred, probabilities, bins=5):
    confidence = probabilities.max(axis=1)
    correct = (pred == np.asarray(y_true)).astype(float)
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (confidence > low) & (confidence <= high)
        if mask.any():
            ece += mask.mean() * abs(correct[mask].mean() - confidence[mask].mean())
    return float(ece)


def repeated_probability_metrics(X, y):
    classes = np.array(sorted(y.unique()))
    cv = RepeatedStratifiedKFold(n_splits=4, n_repeats=10, random_state=SEED)
    fold_rows = []
    class_rows = []
    confusion = {name: np.zeros((len(classes), len(classes)), dtype=int) for name in MODELS}
    for model_name, template in MODELS.items():
        for fold, (train_idx, test_idx) in enumerate(cv.split(X, y)):
            model = clone(template)
            model.fit(X.iloc[train_idx], y.iloc[train_idx])
            pred = model.predict(X.iloc[test_idx])
            probability = model.predict_proba(X.iloc[test_idx])
            y_test = y.iloc[test_idx].to_numpy()
            one_hot = LabelBinarizer().fit(classes).transform(y_test)
            confusion[model_name] += confusion_matrix(y_test, pred, labels=classes)
            precision, recall, class_f1, support = precision_recall_fscore_support(
                y_test, pred, labels=classes, zero_division=0
            )
            for i, label in enumerate(classes):
                class_rows.append({
                    "model": model_name,
                    "fold": fold,
                    "class": label,
                    "precision": precision[i],
                    "recall_sensitivity": recall[i],
                    "f1": class_f1[i],
                    "support": support[i],
                })
            fold_rows.append({
                "model": model_name,
                "fold": fold,
                "accuracy": accuracy_score(y_test, pred),
                "balanced_accuracy": balanced_accuracy_score(y_test, pred),
                "macro_f1": f1_score(y_test, pred, average="macro"),
                "weighted_f1": f1_score(y_test, pred, average="weighted"),
                "matthews_correlation": matthews_corrcoef(y_test, pred),
                "cohen_kappa": cohen_kappa_score(y_test, pred),
                "roc_auc_ovr_macro": roc_auc_score(one_hot, probability, average="macro", multi_class="ovr"),
                "pr_auc_macro": average_precision_score(one_hot, probability, average="macro"),
                "top2_accuracy": top_k_accuracy_score(y_test, probability, k=2, labels=classes),
                "log_loss": log_loss(y_test, probability, labels=classes),
                "multiclass_brier": multiclass_brier(y_test, probability, classes),
                "top_label_ece_5bin": top_label_ece(y_test, pred, probability),
                "mean_confidence": probability.max(axis=1).mean(),
            })
    folds = pd.DataFrame(fold_rows)
    per_class = pd.DataFrame(class_rows)
    metric_columns = [column for column in folds.columns if column not in ("model", "fold")]
    summary_rows = []
    for model_name, subset in folds.groupby("model"):
        row = {"model": model_name}
        for metric in metric_columns:
            row[f"{metric}_mean"] = subset[metric].mean()
            row[f"{metric}_sd"] = subset[metric].std(ddof=1)
            row[f"{metric}_q025"] = subset[metric].quantile(0.025)
            row[f"{metric}_q975"] = subset[metric].quantile(0.975)
        summary_rows.append(row)
    summary = pd.DataFrame(summary_rows).sort_values("macro_f1_mean", ascending=False)
    class_summary = per_class.groupby(["model", "class"]).agg(
        precision_mean=("precision", "mean"),
        precision_sd=("precision", "std"),
        recall_mean=("recall_sensitivity", "mean"),
        recall_sd=("recall_sensitivity", "std"),
        f1_mean=("f1", "mean"),
        f1_sd=("f1", "std"),
    ).reset_index()
    folds.to_csv(TABLES / "repeated_probability_metrics_by_fold.csv", index=False)
    summary.to_csv(TABLES / "repeated_probability_metrics_summary.csv", index=False)
    class_summary.to_csv(TABLES / "per_class_metrics_summary.csv", index=False)
    for model_name, matrix in confusion.items():
        normalized = matrix / matrix.sum(axis=1, keepdims=True)
        safe = model_name.lower().replace(" ", "_")
        pd.DataFrame(matrix, index=classes, columns=classes).to_csv(TABLES / f"confusion_counts_{safe}.csv")
        pd.DataFrame(normalized, index=classes, columns=classes).to_csv(TABLES / f"confusion_normalized_{safe}.csv")
    return folds, summary, class_summary, confusion, classes


def univariate_separability(df, y):
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    rows = []
    for feature in FEATURES:
        for model_name, classifier in (
            ("Decision stump", DecisionTreeClassifier(max_depth=1, random_state=SEED)),
            ("Depth-2 tree", DecisionTreeClassifier(max_depth=2, random_state=SEED)),
            ("Logistic regression", LogisticRegression(max_iter=3000, random_state=SEED)),
        ):
            scores = cross_val_score(
                make_pipeline(classifier, [feature]),
                df[[feature]], y,
                cv=cv, scoring="balanced_accuracy", n_jobs=1,
            )
            rows.append({
                "feature": feature,
                "model": model_name,
                "balanced_accuracy_mean": scores.mean(),
                "balanced_accuracy_sd": scores.std(ddof=1),
            })
    result = pd.DataFrame(rows).sort_values("balanced_accuracy_mean", ascending=False)
    result.to_csv(TABLES / "univariate_feature_separability.csv", index=False)
    return result


def repeated_holdout_seed_sensitivity(X, y):
    from sklearn.model_selection import train_test_split
    rows = []
    for seed in range(100):
        train_x, test_x, train_y, test_y = train_test_split(
            X, y, test_size=0.25, random_state=seed, stratify=y
        )
        model = clone(MODELS["Random Forest"])
        model.fit(train_x, train_y)
        pred = model.predict(test_x)
        rows.append({
            "seed": seed,
            "accuracy": accuracy_score(test_y, pred),
            "macro_f1": f1_score(test_y, pred, average="macro"),
            "matthews_correlation": matthews_corrcoef(test_y, pred),
        })
    result = pd.DataFrame(rows)
    result.to_csv(TABLES / "random_forest_holdout_seed_sensitivity.csv", index=False)
    return result


def figures(summary, class_summary, confusion, classes, holdout, separability):
    sns.set_theme(style="whitegrid", context="talk")
    metrics = ["macro_f1_mean", "matthews_correlation_mean", "cohen_kappa_mean", "pr_auc_macro_mean"]
    plot = summary.set_index("model")[metrics]
    ax = plot.plot(kind="bar", figsize=(12, 6))
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Repeated-CV metric")
    ax.set_title("Metrics beyond accuracy")
    ax.legend(["Macro F1", "MCC", "Cohen kappa", "Macro PR-AUC"], ncol=2)
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES / "metrics_beyond_accuracy.png", dpi=300)
    plt.close()

    rf_matrix = confusion["Random Forest"] / confusion["Random Forest"].sum(axis=1, keepdims=True)
    fig, ax = plt.subplots(figsize=(8, 7))
    sns.heatmap(rf_matrix, annot=True, fmt=".2f", cmap="Blues", xticklabels=classes, yticklabels=classes, ax=ax)
    ax.set_xlabel("Predicted platform")
    ax.set_ylabel("True platform")
    ax.set_title("Random Forest repeated-CV normalized confusion")
    fig.tight_layout()
    fig.savefig(FIGURES / "random_forest_normalized_confusion.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    sns.histplot(holdout["accuracy"], bins=np.linspace(0.3, 1.01, 9), ax=ax)
    ax.axvline(1.0, color="red", linestyle="--", label="Submitted split")
    ax.set_xlabel("Accuracy across 100 stratified hold-out seeds")
    ax.set_title("Random Forest split sensitivity")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "random_forest_holdout_seed_sensitivity.png", dpi=300)
    plt.close(fig)

    top = separability.head(12).sort_values("balanced_accuracy_mean")
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(top["feature"] + " | " + top["model"], top["balanced_accuracy_mean"])
    ax.axvline(1 / 6, color="black", linestyle="--")
    ax.set_xlabel("Balanced accuracy")
    ax.set_title("Single-feature separability embedded in the simulator")
    fig.tight_layout()
    fig.savefig(FIGURES / "univariate_simulator_separability.png", dpi=300)
    plt.close(fig)


def main():
    df = pd.read_csv(DATA)
    distribution = df["Platform"].value_counts().sort_index().rename_axis("platform").reset_index(name="n")
    distribution["proportion"] = distribution["n"] / len(df)
    distribution.to_csv(TABLES / "class_distribution.csv", index=False)
    X = df[FEATURES]
    y = df["Platform"]
    folds, summary, class_summary, confusion, classes = repeated_probability_metrics(X, y)
    separability = univariate_separability(df, y)
    holdout = repeated_holdout_seed_sensitivity(X, y)
    figures(summary, class_summary, confusion, classes, holdout, separability)
    report = {
        "class_counts": dict(zip(distribution["platform"], distribution["n"].astype(int))),
        "balanced_dataset": bool(distribution["n"].nunique() == 1),
        "model_metrics": summary.to_dict(orient="records"),
        "random_forest_holdout_accuracy": {
            "mean": holdout["accuracy"].mean(),
            "sd": holdout["accuracy"].std(ddof=1),
            "min": holdout["accuracy"].min(),
            "max": holdout["accuracy"].max(),
            "perfect_split_frequency": float((holdout["accuracy"] == 1).mean()),
        },
        "top_univariate_signals": separability.head(10).to_dict(orient="records"),
    }
    (OUT / "metric_quality_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
