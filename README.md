# AI-Based Real-Time Cyber Risk Assessment (Prototype)

This is a **working prototype** aligned to your document (a–h). It ingests cybersecurity events, 
trains a model to predict **high-risk** events, and provides a **Streamlit dashboard** for scoring, alerts, and recommendations.

## 🧱 Project Structure
```
cyber-risk-rt/
├── app.py                     # Streamlit dashboard
├── config.yaml                # Threshold & playbook
├── requirements.txt
├── backend/
│   ├── score.py               # Load model and score new events
│   └── train_model.py         # Train RandomForest on sample data
├── data/
│   ├── sample_events.csv      # Synthetic sample data (labeled)
│   └── sample_events_preview.csv
├── models/
│   └── risk_model.pkl         # Trained model (created after training)
└── utils/
    └── recommendations.py     # Playbook loader & suggestions
```

## 🚀 Quickstart
```bash
cd cyber-risk-rt
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt

# 1) Train the model (uses data/sample_events.csv)
python backend/train_model.py

# 2) Run the dashboard
streamlit run app.py
```

Open the URL Streamlit prints (usually http://localhost:8501), then **upload events CSV** (or use the sample).
You’ll see **risk probabilities**, **alerts** when risk >= threshold, and **recommended actions**.

## 📊 Data Schema (columns)
- timestamp, src_ip, dst_ip, event_type, severity
- vuln_count, asset_id, asset_criticality (1–5)
- past_incidents, auth_failures, malware_alerts, anomalous_bytes
- label_high_risk (0/1) — for training only

## 🧠 Model
- scikit-learn **RandomForestClassifier** in a preprocessing pipeline (OneHotEncoder + imputation).
- Predicts probability of **high risk**.

## 🔔 Alerts & Recommendations
- Threshold set in `config.yaml` (default 0.7) or adjustable in the app.
- Recommendations come from `utils/recommendations.py` + `config.yaml` playbook.

## 🔧 Next Steps (future enhancements)
- Replace synthetic data with **real SIEM/EDR/Vuln scan feeds**.
- Add **Kafka** or **FastAPI** for real-time streaming.
- Add **financial impact** and **what-if** simulations.
- Export to **Power BI/Tableau** or integrate with **GRC** tools.
