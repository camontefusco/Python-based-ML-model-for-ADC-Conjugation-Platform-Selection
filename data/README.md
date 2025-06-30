# Dataset Description for ADC Conjugation Synthetic Advanced

## Overview
This folder contains the primary dataset used for exploring and modeling ADC (Antibody-Drug Conjugate) conjugation technologies.

### File:
- `adc_conjugation_synthetic_advanced.csv`  
  A synthetic dataset simulating real-world ADC conjugation platform metrics, designed to mimic published data from companies like Genentech, Synaffix, WuXi, and others.

## Dataset Contents
The dataset includes multiple rows per conjugation platform to simulate batch variability and contains the following columns:

| Column               | Description                                                                                          |
|----------------------|----------------------------------------------------------------------------------------------------|
| Technology_Category  | Category of conjugation technology (e.g., Random, Site-Specific Non-Selective, Site-Specific Selective) |
| Platform             | Specific conjugation platform name (e.g., Lysine-Based, THIOMAB™, WuXiDAR4™)                        |
| Vendor               | Platform vendor or developer                                                                        |
| DAR_Mean             | Mean Drug-to-Antibody Ratio                                                                         |
| DAR_Std              | Standard deviation of DAR                                                                           |
| DAR_CV               | Coefficient of Variation of DAR                                                                     |
| Homogeneity          | Score indicating conjugation uniformity                                                            |
| Stability_Score      | Proxy score reflecting chemical/biological stability                                               |
| Expression_Ease      | Ease of protein expression for the platform                                                        |
| Cost_Index           | Cost indicator inversely related to expression ease                                                |
| CMC_Risk             | Manufacturing risk category (Low, Medium, High)                                                    |
| Scalability          | Manufacturability score (0 to 1)                                                                    |
| Latency_to_Clinic_yrs| Estimated years to clinic readiness                                                                |
| Approved_Usage       | List of approved ADC drugs using this platform                                                     |

## Data Generation Notes
- Data is synthetically generated based on 2025 ADC technology reviews and public literature (e.g., [Antibody Therapeutics, 2025](https://academic.oup.com/abt/article/8/2/157/8115463)).  
- Metrics reflect realistic trade-offs between performance, manufacturability, and cost considerations.  
- Multiple batches simulated per platform to capture variability.

## Usage
- Ideal for multi-criteria decision modeling, platform comparison, and machine learning model training.  
- Can be combined with provided notebooks for analysis, model building, and platform recommendation.

## License & Attribution
Synthetic data inspired by real-world ADC conjugation technologies; intended for research and educational use.

