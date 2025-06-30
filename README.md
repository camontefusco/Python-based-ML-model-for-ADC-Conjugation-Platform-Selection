# adc-conjugation-guide
A curated guide and decision-support tool to aid scientists in selecting optimal conjugation strategies for antibody-drug conjugates (ADCs), including summaries of current technologies, platform comparisons, and use-case recommendations.

# ADC Conjugation Platform Recommender

This repository provides a structured, practical resource for selecting the right conjugation method for antibody-drug conjugates (ADCs). It is based on the 2025 review by WuXi XDC and includes comparative analysis of Random, Site-Specific Non-Selective, and Site-Specific Selective technologies.

## 🧠 Features

- Technology overviews and pros/cons
- Decision trees and scoring templates
- DAR (Drug-Antibody Ratio) calculation tools
- Summary of platforms like WuXiDAR4™, SMARTag®, THIOMAB™, etc.
- Peer-reviewed references for in-depth reading

## 📊 Quick Comparison

| Strategy                          | DAR Control | Complexity | Scalability | Homogeneity | Example Platforms        |
|----------------------------------|-------------|------------|-------------|-------------|--------------------------|
| Random Conjugation               | Low         | Low        | High        | Low         | NHS-Lysine, Maleimide    |
| Site-Specific, Non-Selective     | Medium      | Medium     | Medium      | Medium      | GlycoConnect™, Enzymatic |
| Site-Specific and Selective      | High        | High       | Medium      | High        | WuXiDAR4™, THIOMAB™      |

## 📊 ML Prediction Flow Diagram

╔══════════════════════════════════════════════╗
║     🧪 User Inputs (via Gradio Interface)     ║
╠══════════════════════════════════════════════╣
║ - Technology_Category                        ║
║ - DAR_Mean, DAR_Std, DAR_CV                  ║
║ - Stability_Score, Expression_Ease           ║
║ - Homogeneity, Cost_Index                    ║
║ - CMC_Risk, Approved_Usage, Vendor           ║
║ - Scalability, Latency_to_Clinic_yrs         ║
╚══════════════════════════════════════════════╝
                │
                ▼
╔══════════════════════════════════════════════╗
║     🧹 Data Preprocessing Pipeline (in .pkl)  ║
╠══════════════════════════════════════════════╣
║ - Convert categoricals to string             ║
║ - One-hot / ordinal encoding                 ║
║ - Normalize/scale numerical values           ║
╚══════════════════════════════════════════════╝
                │
                ▼
╔══════════════════════════════════════════════╗
║     🧠 Trained ML Model (e.g., Random Forest) ║
╠══════════════════════════════════════════════╣
║ - Trained on historical ADC project data     ║
║ - Learns platform suitability from patterns  ║
║ - Outputs platform label                     ║
╚══════════════════════════════════════════════╝
                │
                ▼
╔══════════════════════════════════════════════╗
║   ✅ Predicted Conjugation Platform Label     ║
╠══════════════════════════════════════════════╣
║ Example: "Lysine-Based"                      ║
║ Displayed in Gradio interface                ║
║ Exported in a downloadable PDF report        ║
╚══════════════════════════════════════════════╝


## 🔍 References

See [`references/key_publications.md`](references/key_publications.md) for foundational and recent literature, including:

- WuXi XDC, *Antibody Therapeutics* (2025)
- Beck et al., *Nat Rev Drug Discov* (2020)
