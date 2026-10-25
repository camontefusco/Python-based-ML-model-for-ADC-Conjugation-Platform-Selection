"""Local Gradio demonstration for the synthetic ADC platform benchmark."""
from pathlib import Path
import datetime
import os
import joblib
import pandas as pd
import gradio as gr
from fpdf import FPDF

ROOT = Path(__file__).resolve().parent
MODEL = joblib.load(ROOT / "models" / "rf_adc_pipeline.pkl")
REPORT = ROOT / "reports" / "adc_platform_report_demo.pdf"

def predict_and_report(tech_cat, dar_mean, dar_std, dar_cv, stability,
                       expression, homogeneity, cost, cmc_risk, usage,
                       vendor, scalability, latency):
    values = {
        "Technology_Category": tech_cat, "DAR_Mean": float(dar_mean),
        "DAR_Std": float(dar_std), "DAR_CV": float(dar_cv),
        "Stability_Score": float(stability), "Expression_Ease": float(expression),
        "Homogeneity": float(homogeneity), "Cost_Index": float(cost),
        "CMC_Risk": cmc_risk, "Approved_Usage": usage, "Vendor": vendor,
        "Scalability": float(scalability), "Latency_to_Clinic_yrs": float(latency),
    }
    frame = pd.DataFrame([values])
    for col in ("Technology_Category", "CMC_Risk", "Approved_Usage", "Vendor"):
        frame[col] = frame[col].astype(str)
    prediction = MODEL.predict(frame)[0]
    report = FPDF()
    report.add_page()
    report.set_font("Arial", "B", 16)
    report.cell(190, 10, "ADC Conjugation Platform Report", ln=True, align="C")
    report.set_font("Arial", size=11)
    report.ln(8)
    report.cell(190, 8, f"Generated on: {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", ln=True)
    report.ln(5)
    for key, value in values.items():
        report.cell(190, 7, f"{key}: {value}", ln=True)
    report.ln(6)
    report.set_font("Arial", "B", 13)
    # FPDF 1.x writes Latin-1; normalize platform labels for the PDF only.
    pdf_prediction = str(prediction).replace("™", "(TM)")
    report.cell(190, 9, f"Recommended Platform: {pdf_prediction}", ln=True)
    REPORT.parent.mkdir(exist_ok=True)
    report.output(str(REPORT))
    return f"Recommended Platform: {prediction}\nPDF report generated successfully."

demo = gr.Interface(
    fn=predict_and_report,
    inputs=[
        gr.Slider(0, 2, step=1, value=1, label="Technology_Category (0–2)"),
        gr.Slider(2.0, 4.5, step=0.1, value=3.5, label="DAR_Mean"),
        gr.Slider(0.1, 1.0, step=0.01, value=0.5, label="DAR_Std"),
        gr.Slider(0.01, 0.5, step=0.01, value=0.15, label="DAR_CV"),
        gr.Slider(0.0, 10.0, step=0.1, value=7.0, label="Stability_Score"),
        gr.Slider(0.0, 1.0, step=0.05, value=0.7, label="Expression_Ease"),
        gr.Slider(0.0, 1.0, step=0.05, value=0.8, label="Homogeneity"),
        gr.Slider(0.0, 1.0, step=0.05, value=0.4, label="Cost_Index"),
        gr.Dropdown([0, 1, 2], value=1, label="CMC_Risk (0=Low, 1=Medium, 2=High)"),
        gr.Radio([0, 1], value=1, label="Approved_Usage (0=No, 1=Yes)"),
        gr.Dropdown([0, 1, 2], value=1, label="Vendor (0–2)"),
        gr.Slider(0.0, 1.0, step=0.05, value=0.7, label="Scalability"),
        gr.Slider(0.0, 10.0, step=0.1, value=3.0, label="Latency_to_Clinic_yrs"),
    ],
    outputs=gr.Textbox(label="Result"),
    title="ADC Platform Recommender",
    description="Demonstration interface for the synthetic benchmark workflow. Outputs are not validated clinical or manufacturing decisions.",
)

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=int(os.environ.get("GRADIO_SERVER_PORT", "7860")), share=False)
