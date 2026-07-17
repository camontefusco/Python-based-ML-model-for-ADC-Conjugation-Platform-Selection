from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import binomtest
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, matthews_corrcoef
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "adc_conjugation_synthetic_advanced.csv"
VALIDATION_PATH = ROOT / "data" / "literature_validation_20.csv"
OUT = ROOT / "reports" / "validation_20_audit"
TABLES = OUT / "tables"
FIGURES = OUT / "figures"
for folder in (TABLES, FIGURES):
    folder.mkdir(parents=True, exist_ok=True)

SEED = 42
OBJECTIVE_FEATURES = ["DAR_Mean", "DAR_CV"]
HARMONIZED_FEATURES = ["DAR_Mean", "DAR_CV", "Stability_Score", "Homogeneity", "Scalability"]

# Metadata reproduces the validation notebook's submitted curation state. It is
# retained separately from current regulatory status to avoid post-submission drift.
METADATA = {
    "Gemtuzumab ozogamicin (Mylotarg)": (2017, "regulatory_plus_publication"),
    "Brentuximab vedotin (Adcetris)": (2011, "regulatory_plus_publication"),
    "Ado-trastuzumab emtansine (Kadcyla / T-DM1)": (2013, "regulatory_plus_publication"),
    "Inotuzumab ozogamicin (Besponsa)": (2017, "regulatory_plus_publication"),
    "Polatuzumab vedotin (Polivy)": (2019, "regulatory_plus_publication"),
    "Enfortumab vedotin (Padcev)": (2019, "regulatory_plus_publication"),
    "Sacituzumab govitecan (Trodelvy)": (2020, "regulatory_plus_publication"),
    "Belantamab mafodotin (Blenrep)": (2020, "regulatory_plus_publication"),
    "Trastuzumab deruxtecan (Enhertu / T-DXd)": (2019, "regulatory_plus_publication"),
    "Loncastuximab tesirine (Zynlonta)": (2021, "regulatory_plus_publication"),
    "Tisotumab vedotin (Tivdak)": (2021, "regulatory_plus_publication"),
    "Mirvetuximab soravtansine (Elahere)": (2022, "regulatory_plus_publication"),
    "Datopotamab deruxtecan (Dato-DXd)": (2025, "regulatory_plus_publication"),
    "Patritumab deruxtecan (HER3-DXd)": (2024, "clinical_publication"),
    "Telisotuzumab vedotin (Teliso-V)": (2025, "regulatory_plus_publication"),
    "Zilovertamab vedotin (ZV)": (2023, "clinical_publication"),
    "Upifitamab rilsodotin (UpRi)": (2023, "clinical_publication"),
    "SGN-B6A (ladiratuzumab vedotin variant)": (2021, "clinical_publication"),
    "ADCT-601 (camidanlumab tesirine / Cami-T)": (2021, "clinical_publication"),
    "XMT-1592 (upifitamab rilsodotin precursor)": (2019, "clinical_publication"),
}


def model_pipeline(features, estimator):
    prep = ColumnTransformer([
        ("numeric", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]), features)
    ])
    return Pipeline([("preprocessing", prep), ("classifier", estimator)])


def wilson(correct, total):
    ci = binomtest(int(correct), int(total)).proportion_ci(0.95, method="wilson")
    return float(ci.low), float(ci.high)


def prepare_validation():
    validation = pd.read_csv(VALIDATION_PATH)
    validation["evidence_year"] = validation["name"].map(lambda value: METADATA[value][0])
    validation["source_group"] = validation["name"].map(lambda value: METADATA[value][1])
    validation["temporal_cohort"] = pd.cut(
        validation["evidence_year"],
        bins=[0, 2020, 2022, 9999],
        labels=["through_2020", "2021_to_2022", "2023_or_later"],
    ).astype(str)
    validation["DAR_Mean"] = validation["dar_mean"]
    validation["DAR_CV"] = validation["dar_cv"]
    validation["Stability_Score"] = validation["stability_score"] / 5.0
    validation["Homogeneity"] = validation["homogeneity_score"] / 5.0
    validation["Scalability"] = validation["manufacturability"] / 5.0
    validation["has_subjective_harmonization"] = True
    return validation


def ood_audit(training, validation, features, prefix):
    train = training[features].copy()
    external = validation[features].copy()
    scaler = StandardScaler().fit(train)
    train_z = scaler.transform(train)
    external_z = scaler.transform(external)
    train_nn = NearestNeighbors(n_neighbors=2).fit(train_z)
    train_distances = train_nn.kneighbors(train_z)[0][:, 1]
    threshold = float(np.quantile(train_distances, 0.95))
    external_nn = NearestNeighbors(n_neighbors=1).fit(train_z)
    external_distance = external_nn.kneighbors(external_z)[0][:, 0]

    range_count = np.zeros(len(validation), dtype=int)
    range_distance = np.zeros(len(validation), dtype=float)
    feature_rows = []
    for feature in features:
        low = float(train[feature].min())
        high = float(train[feature].max())
        span = high - low
        below = np.maximum(low - external[feature].to_numpy(), 0)
        above = np.maximum(external[feature].to_numpy() - high, 0)
        out = (below + above) > 0
        range_count += out.astype(int)
        if span > 0:
            range_distance += (below + above) / span
        feature_rows.append({
            "feature_set": prefix,
            "feature": feature,
            "training_min": low,
            "training_max": high,
            "external_min": float(external[feature].min()),
            "external_max": float(external[feature].max()),
            "external_n_outside_range": int(out.sum()),
        })
        validation[f"{prefix}_{feature}_outside_range"] = out
    validation[f"{prefix}_n_features_outside_range"] = range_count
    validation[f"{prefix}_normalized_range_exceedance"] = range_distance
    validation[f"{prefix}_nearest_neighbor_z_distance"] = external_distance
    validation[f"{prefix}_nn_ood_threshold"] = threshold
    validation[f"{prefix}_ood_by_nn"] = external_distance > threshold
    validation[f"{prefix}_ood_any"] = (range_count > 0) | (external_distance > threshold)
    return pd.DataFrame(feature_rows)


def evaluate_models(training, validation, features, feature_set):
    estimators = {
        "Logistic regression": LogisticRegression(
            max_iter=3000, class_weight="balanced", random_state=SEED
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=1000, class_weight="balanced", random_state=SEED, n_jobs=1
        ),
        "Extra Trees": ExtraTreesClassifier(
            n_estimators=1000, class_weight="balanced", random_state=SEED, n_jobs=1
        ),
    }
    labels = sorted(training["Technology_Category"].unique())
    prediction_columns = []
    summary_rows = []
    for name, estimator in estimators.items():
        model = model_pipeline(features, estimator)
        model.fit(training[features], training["Technology_Category"])
        prediction = model.predict(validation[features])
        probability = model.predict_proba(validation[features])
        safe = name.lower().replace(" ", "_")
        column = f"{feature_set}_{safe}_prediction"
        prediction_columns.append(column)
        validation[column] = prediction
        validation[f"{feature_set}_{safe}_confidence"] = probability.max(axis=1)
        validation[f"{feature_set}_{safe}_correct"] = prediction == validation["platform_category"]
        correct = int(validation[f"{feature_set}_{safe}_correct"].sum())
        low, high = wilson(correct, len(validation))
        summary_rows.append({
            "feature_set": feature_set,
            "model": name,
            "features": "; ".join(features),
            "correct": correct,
            "total": len(validation),
            "accuracy": accuracy_score(validation["platform_category"], prediction),
            "macro_f1": f1_score(validation["platform_category"], prediction, average="macro"),
            "mcc": matthews_corrcoef(validation["platform_category"], prediction),
            "wilson_95_low": low,
            "wilson_95_high": high,
        })
        matrix = pd.DataFrame(
            confusion_matrix(validation["platform_category"], prediction, labels=labels),
            index=labels, columns=labels,
        )
        matrix.to_csv(TABLES / f"confusion_{feature_set}_{safe}.csv")
    validation[f"{feature_set}_model_consensus"] = validation[prediction_columns].nunique(axis=1) == 1
    return pd.DataFrame(summary_rows)


def subgroup_summary(validation, feature_set, model_name, grouping):
    safe = model_name.lower().replace(" ", "_")
    correct_col = f"{feature_set}_{safe}_correct"
    rows = []
    for group, subset in validation.groupby(grouping, observed=True):
        correct = int(subset[correct_col].sum())
        total = len(subset)
        low, high = wilson(correct, total)
        rows.append({
            "feature_set": feature_set,
            "model": model_name,
            "grouping": grouping,
            "group": str(group),
            "correct": correct,
            "total": total,
            "concordance": correct / total,
            "wilson_95_low": low,
            "wilson_95_high": high,
        })
    return pd.DataFrame(rows)


def make_figures(validation, summaries, subgroup):
    sns.set_theme(style="whitegrid", context="talk")
    fig, ax = plt.subplots(figsize=(9, 5.5))
    plot = summaries.copy()
    plot["label"] = plot["feature_set"] + " | " + plot["model"]
    sns.barplot(data=plot, x="accuracy", y="label", ax=ax)
    ax.set_xlim(0, 1)
    ax.set_xlabel("20-ADC concordance")
    ax.set_ylabel("")
    ax.set_title("Objective-only versus harmonized-feature assessment")
    fig.tight_layout()
    fig.savefig(FIGURES / "validation_model_comparison.png", dpi=300)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(
        data=validation,
        x="objective_nearest_neighbor_z_distance",
        y="dar_mean",
        hue="platform_category",
        style="objective_ood_any",
        s=110,
        ax=ax,
    )
    ax.axvline(validation["objective_nn_ood_threshold"].iloc[0], color="black", linestyle="--")
    ax.set_xlabel("Nearest synthetic record distance (standardized objective space)")
    ax.set_ylabel("Literature DAR mean")
    ax.set_title("Applicability-domain audit of the 20 literature ADCs")
    fig.tight_layout()
    fig.savefig(FIGURES / "validation_ood_distance.png", dpi=300)
    plt.close(fig)

    selected = subgroup[(subgroup["feature_set"] == "objective") & (subgroup["model"] == "Random Forest")]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.barplot(data=selected, x="concordance", y="group", hue="grouping", ax=ax)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Concordance")
    ax.set_ylabel("")
    ax.set_title("Temporal and source-stratified stress test")
    fig.tight_layout()
    fig.savefig(FIGURES / "validation_temporal_source_subgroups.png", dpi=300)
    plt.close(fig)


def main():
    training = pd.read_csv(TRAIN_PATH)
    validation = prepare_validation()
    range_tables = [
        ood_audit(training, validation, OBJECTIVE_FEATURES, "objective"),
        ood_audit(training, validation, HARMONIZED_FEATURES, "harmonized"),
    ]
    summaries = pd.concat([
        evaluate_models(training, validation, OBJECTIVE_FEATURES, "objective"),
        evaluate_models(training, validation, HARMONIZED_FEATURES, "harmonized"),
    ], ignore_index=True)
    subgroup = pd.concat([
        subgroup_summary(validation, feature_set, model, grouping)
        for feature_set in ("objective", "harmonized")
        for model in ("Logistic regression", "Random Forest", "Extra Trees")
        for grouping in ("temporal_cohort", "source_group", "platform_category")
    ], ignore_index=True)

    validation.to_csv(TABLES / "validation_20_record_level_audit.csv", index=False)
    summaries.to_csv(TABLES / "validation_20_model_summary.csv", index=False)
    subgroup.to_csv(TABLES / "validation_20_temporal_source_subgroups.csv", index=False)
    pd.concat(range_tables, ignore_index=True).to_csv(TABLES / "validation_20_feature_range_audit.csv", index=False)
    make_figures(validation, summaries, subgroup)

    objective_rf = summaries[(summaries["feature_set"] == "objective") & (summaries["model"] == "Random Forest")].iloc[0]
    harmonized_rf = summaries[(summaries["feature_set"] == "harmonized") & (summaries["model"] == "Random Forest")].iloc[0]
    report = {
        "validation_records": len(validation),
        "objective_features": OBJECTIVE_FEATURES,
        "harmonized_features": HARMONIZED_FEATURES,
        "objective_rf": objective_rf.to_dict(),
        "harmonized_rf": harmonized_rf.to_dict(),
        "objective_ood_records": int(validation["objective_ood_any"].sum()),
        "harmonized_ood_records": int(validation["harmonized_ood_any"].sum()),
        "objective_model_consensus_records": int(validation["objective_model_consensus"].sum()),
        "harmonized_model_consensus_records": int(validation["harmonized_model_consensus"].sum()),
        "required_statement": (
            "This literature-derived analysis is a transportability and applicability-domain stress test, not definitive external validation. "
            "The source data are sparse, partly harmonized from qualitative scores, and frequently outside the synthetic training domain. "
            "Prospective validation using independently measured ADC development records remains required before practical use."
        ),
    }
    (OUT / "validation_20_summary.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
