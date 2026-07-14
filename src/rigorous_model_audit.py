from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import (
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    log_loss,
)
from sklearn.model_selection import (
    GridSearchCV,
    RepeatedStratifiedKFold,
    StratifiedKFold,
    cross_validate,
    learning_curve,
)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "adc_conjugation_synthetic_advanced.csv"
OUT = ROOT / "reports" / "rigorous_model_audit"
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
    prep = ColumnTransformer(
        [("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), FEATURES)],
        remainder="drop",
    )
    return Pipeline([("preprocessing", prep), ("classifier", estimator)])


MODELS = {
    "Dummy (stratified)": pipeline(DummyClassifier(strategy="stratified", random_state=SEED)),
    "Logistic regression": pipeline(LogisticRegression(max_iter=3000, C=1.0, random_state=SEED)),
    "Linear SVM": pipeline(SVC(kernel="linear", C=1.0, probability=True, random_state=SEED)),
    "RBF SVM": pipeline(SVC(kernel="rbf", C=1.0, gamma="scale", probability=True, random_state=SEED)),
    "k-nearest neighbors": pipeline(KNeighborsClassifier(n_neighbors=5, weights="distance")),
    "Decision tree": pipeline(DecisionTreeClassifier(random_state=SEED)),
    "Random Forest": pipeline(RandomForestClassifier(
        n_estimators=300, class_weight="balanced", random_state=SEED, n_jobs=1
    )),
    "Extra Trees": pipeline(ExtraTreesClassifier(
        n_estimators=300, class_weight="balanced", random_state=SEED, n_jobs=1
    )),
    "Gradient Boosting": pipeline(GradientBoostingClassifier(
        n_estimators=150, learning_rate=0.05, max_depth=2, random_state=SEED
    )),
}


def q025(values):
    return float(np.quantile(values, 0.025))


def q975(values):
    return float(np.quantile(values, 0.975))


def repeated_cv_benchmark(X, y):
    cv = RepeatedStratifiedKFold(n_splits=4, n_repeats=10, random_state=SEED)
    rows = []
    fold_rows = []
    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": "balanced_accuracy",
        "macro_f1": "f1_macro",
        "neg_log_loss": "neg_log_loss",
        "roc_auc_ovr": "roc_auc_ovr",
    }
    for name, model in MODELS.items():
        result = cross_validate(
            model,
            X,
            y,
            cv=cv,
            scoring=scoring,
            return_train_score=True,
            n_jobs=1,
            error_score="raise",
        )
        for fold in range(len(result["test_accuracy"])):
            fold_rows.append({
                "model": name,
                "fold": fold,
                "train_accuracy": result["train_accuracy"][fold],
                "validation_accuracy": result["test_accuracy"][fold],
                "generalization_gap": result["train_accuracy"][fold] - result["test_accuracy"][fold],
                "validation_macro_f1": result["test_macro_f1"][fold],
                "validation_log_loss": -result["test_neg_log_loss"][fold],
                "validation_roc_auc_ovr": result["test_roc_auc_ovr"][fold],
            })
        test_acc = result["test_accuracy"]
        train_acc = result["train_accuracy"]
        rows.append({
            "model": name,
            "train_accuracy_mean": train_acc.mean(),
            "validation_accuracy_mean": test_acc.mean(),
            "validation_accuracy_sd": test_acc.std(ddof=1),
            "validation_accuracy_q025": q025(test_acc),
            "validation_accuracy_q975": q975(test_acc),
            "generalization_gap_mean": (train_acc - test_acc).mean(),
            "macro_f1_mean": result["test_macro_f1"].mean(),
            "balanced_accuracy_mean": result["test_balanced_accuracy"].mean(),
            "roc_auc_ovr_mean": result["test_roc_auc_ovr"].mean(),
            "log_loss_mean": (-result["test_neg_log_loss"]).mean(),
        })
    summary = pd.DataFrame(rows).sort_values("validation_accuracy_mean", ascending=False)
    folds = pd.DataFrame(fold_rows)
    summary.to_csv(TABLES / "repeated_cv_model_benchmark.csv", index=False)
    folds.to_csv(TABLES / "repeated_cv_fold_results.csv", index=False)
    return summary, folds


def nested_cv_random_forest(X, y):
    outer = RepeatedStratifiedKFold(n_splits=4, n_repeats=5, random_state=SEED)
    inner = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED)
    base = pipeline(RandomForestClassifier(
        class_weight="balanced", random_state=SEED, n_jobs=1
    ))
    grid = {
        "classifier__n_estimators": [150],
        "classifier__max_depth": [2, 4, None],
        "classifier__min_samples_leaf": [1, 2, 4],
        "classifier__max_features": ["sqrt", 0.7],
    }
    rows = []
    for fold, (train_idx, test_idx) in enumerate(outer.split(X, y)):
        search = GridSearchCV(base, grid, scoring="balanced_accuracy", cv=inner, n_jobs=1)
        search.fit(X.iloc[train_idx], y.iloc[train_idx])
        pred_train = search.predict(X.iloc[train_idx])
        pred_test = search.predict(X.iloc[test_idx])
        rows.append({
            "outer_fold": fold,
            "inner_best_score": search.best_score_,
            "train_accuracy": accuracy_score(y.iloc[train_idx], pred_train),
            "outer_accuracy": accuracy_score(y.iloc[test_idx], pred_test),
            "outer_balanced_accuracy": balanced_accuracy_score(y.iloc[test_idx], pred_test),
            "outer_macro_f1": f1_score(y.iloc[test_idx], pred_test, average="macro"),
            "generalization_gap": accuracy_score(y.iloc[train_idx], pred_train) - accuracy_score(y.iloc[test_idx], pred_test),
            "best_params": json.dumps(search.best_params_, sort_keys=True),
        })
    result = pd.DataFrame(rows)
    result.to_csv(TABLES / "nested_cv_random_forest.csv", index=False)
    return result


def learning_curve_analysis(X, y):
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    model = MODELS["Random Forest"]
    sizes, train_scores, val_scores = learning_curve(
        model,
        X,
        y,
        train_sizes=[0.50, 0.67, 0.83, 1.0],
        cv=cv,
        scoring="accuracy",
        shuffle=True,
        random_state=SEED,
        n_jobs=1,
    )
    rows = []
    for i, size in enumerate(sizes):
        rows.append({
            "training_examples": int(size),
            "train_accuracy_mean": train_scores[i].mean(),
            "train_accuracy_sd": train_scores[i].std(ddof=1),
            "validation_accuracy_mean": val_scores[i].mean(),
            "validation_accuracy_sd": val_scores[i].std(ddof=1),
            "generalization_gap": train_scores[i].mean() - val_scores[i].mean(),
        })
    result = pd.DataFrame(rows)
    result.to_csv(TABLES / "random_forest_learning_curve.csv", index=False)
    return result


def noise_stress_test(X, y):
    cv = StratifiedKFold(n_splits=4, shuffle=True, random_state=SEED)
    scales = [0.0, 0.05, 0.10, 0.20, 0.35]
    rows = []
    feature_sd = X.std(ddof=1)
    for noise_scale in scales:
        for repeat in range(10):
            rng = np.random.default_rng(SEED + repeat)
            for fold, (train_idx, test_idx) in enumerate(cv.split(X, y)):
                model = clone(MODELS["Random Forest"])
                model.fit(X.iloc[train_idx], y.iloc[train_idx])
                noisy = X.iloc[test_idx].copy()
                if noise_scale:
                    noisy += rng.normal(0, feature_sd.to_numpy() * noise_scale, size=noisy.shape)
                pred = model.predict(noisy)
                proba = model.predict_proba(noisy)
                rows.append({
                    "noise_sd_fraction": noise_scale,
                    "repeat": repeat,
                    "fold": fold,
                    "accuracy": accuracy_score(y.iloc[test_idx], pred),
                    "macro_f1": f1_score(y.iloc[test_idx], pred, average="macro"),
                    "log_loss": log_loss(y.iloc[test_idx], proba, labels=model.classes_),
                })
    result = pd.DataFrame(rows)
    result.to_csv(TABLES / "random_forest_noise_stress_test.csv", index=False)
    return result


def importance_stability(X, y):
    rng = np.random.default_rng(SEED)
    rows = []
    rank_vectors = []
    for replicate in range(50):
        sample_idx = rng.integers(0, len(X), len(X))
        inbag = np.zeros(len(X), dtype=bool)
        inbag[np.unique(sample_idx)] = True
        oob_idx = np.where(~inbag)[0]
        if len(oob_idx) < 8 or y.iloc[sample_idx].nunique() < y.nunique():
            continue
        model = pipeline(RandomForestClassifier(
            n_estimators=200, class_weight="balanced", random_state=SEED + replicate, n_jobs=1
        ))
        model.fit(X.iloc[sample_idx], y.iloc[sample_idx])
        mdi = model.named_steps["classifier"].feature_importances_
        perm = permutation_importance(
            model, X.iloc[oob_idx], y.iloc[oob_idx],
            scoring="balanced_accuracy", n_repeats=10,
            random_state=SEED + replicate, n_jobs=1,
        ).importances_mean
        ranks = pd.Series(perm, index=FEATURES).rank(ascending=False, method="average")
        rank_vectors.append(ranks.to_numpy())
        for i, feature in enumerate(FEATURES):
            rows.append({
                "replicate": replicate,
                "feature": feature,
                "mdi_importance": mdi[i],
                "oob_permutation_importance": perm[i],
                "permutation_rank": ranks[feature],
            })
    result = pd.DataFrame(rows)
    result.to_csv(TABLES / "feature_importance_bootstrap_stability.csv", index=False)
    correlations = []
    for i in range(len(rank_vectors)):
        for j in range(i + 1, len(rank_vectors)):
            correlations.append(spearmanr(rank_vectors[i], rank_vectors[j]).statistic)
    summary = result.groupby("feature").agg(
        mdi_mean=("mdi_importance", "mean"),
        mdi_sd=("mdi_importance", "std"),
        permutation_mean=("oob_permutation_importance", "mean"),
        permutation_sd=("oob_permutation_importance", "std"),
        median_rank=("permutation_rank", "median"),
        rank_sd=("permutation_rank", "std"),
        top3_frequency=("permutation_rank", lambda x: float((x <= 3).mean())),
    ).reset_index().sort_values("median_rank")
    summary["pairwise_rank_spearman_mean"] = np.nanmean(correlations)
    summary["pairwise_rank_spearman_sd"] = np.nanstd(correlations, ddof=1)
    summary.to_csv(TABLES / "feature_importance_stability_summary.csv", index=False)
    return result, summary


def create_figures(benchmark, folds, learning, noise, importance_summary):
    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(11, 7))
    order = benchmark.sort_values("validation_accuracy_mean")["model"]
    sns.boxplot(data=folds, x="validation_accuracy", y="model", order=order, ax=ax)
    ax.axvline(1 / 6, color="black", linestyle="--", linewidth=1, label="Six-class chance")
    ax.set_title("Repeated cross-validation across model families")
    ax.set_xlabel("Validation accuracy")
    ax.set_ylabel("")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(FIGURES / "model_benchmark_accuracy.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.errorbar(
        learning["training_examples"], learning["train_accuracy_mean"],
        yerr=learning["train_accuracy_sd"], marker="o", label="Training"
    )
    ax.errorbar(
        learning["training_examples"], learning["validation_accuracy_mean"],
        yerr=learning["validation_accuracy_sd"], marker="o", label="Validation"
    )
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Training examples")
    ax.set_ylabel("Accuracy")
    ax.set_title("Random Forest learning curve")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES / "random_forest_learning_curve.png", dpi=300)
    plt.close(fig)

    noise_summary = noise.groupby("noise_sd_fraction")["accuracy"].agg(["mean", "std"]).reset_index()
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.errorbar(noise_summary["noise_sd_fraction"], noise_summary["mean"], yerr=noise_summary["std"], marker="o")
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Gaussian perturbation (fraction of feature SD)")
    ax.set_ylabel("Validation accuracy")
    ax.set_title("Random Forest sensitivity to measurement noise")
    fig.tight_layout()
    fig.savefig(FIGURES / "random_forest_noise_sensitivity.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    plot = importance_summary.sort_values("median_rank", ascending=False)
    ax.barh(plot["feature"], plot["permutation_mean"], xerr=plot["permutation_sd"])
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("OOB permutation importance (mean +/- SD)")
    ax.set_title("Feature importance stability across bootstrap fits")
    fig.tight_layout()
    fig.savefig(FIGURES / "feature_importance_stability.png", dpi=300)
    plt.close(fig)


def main():
    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y = df["Platform"]
    benchmark, folds = repeated_cv_benchmark(X, y)
    nested = nested_cv_random_forest(X, y)
    learning = learning_curve_analysis(X, y)
    noise = noise_stress_test(X, y)
    _, importance_summary = importance_stability(X, y)
    create_figures(benchmark, folds, learning, noise, importance_summary)

    rf = benchmark.loc[benchmark["model"] == "Random Forest"].iloc[0]
    dummy = benchmark.loc[benchmark["model"] == "Dummy (stratified)"].iloc[0]
    best = benchmark.iloc[0]
    audit = {
        "n_records": len(df),
        "n_classes": y.nunique(),
        "features": FEATURES,
        "best_repeated_cv_model": best.to_dict(),
        "random_forest_repeated_cv": rf.to_dict(),
        "dummy_repeated_cv": dummy.to_dict(),
        "nested_rf_outer_accuracy_mean": nested["outer_accuracy"].mean(),
        "nested_rf_outer_accuracy_sd": nested["outer_accuracy"].std(ddof=1),
        "nested_rf_generalization_gap_mean": nested["generalization_gap"].mean(),
        "learning_curve_final": learning.iloc[-1].to_dict(),
        "noise_accuracy_by_level": noise.groupby("noise_sd_fraction")["accuracy"].mean().to_dict(),
        "importance_rank_spearman_mean": importance_summary["pairwise_rank_spearman_mean"].iloc[0],
        "importance_stability": importance_summary.to_dict(orient="records"),
        "interpretation": (
            "Internal discrimination exceeds a dummy baseline, but high training accuracy, positive generalization gaps, "
            "wide repeated-fold distributions, unstable resampled importance rankings, synthetic class construction, "
            "and out-of-domain literature records preclude claims of real-world predictive validity."
        ),
    }
    (OUT / "audit_summary.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(json.dumps(audit, indent=2))


if __name__ == "__main__":
    main()
