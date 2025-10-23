---

# AI-Based Real-Time Cyber Risk Assessment

Experience **real-time cyber risk assessment** with this interactive prototype. It ingests cybersecurity event data, predicts **high-risk incidents**, and provides actionable recommendations via a **user-friendly Streamlit dashboard**.

**Try it online:** https://secure-risk1-ai.streamlit.app/

---

## Overview

This prototype helps security teams **prioritize threats** and **mitigate risks** efficiently. Key features include:

* **Risk Scoring:** Predicts probability of high-risk events using a RandomForest model.
* **Alerts:** Flags critical events automatically based on configurable thresholds.
* **Recommendations:** Provides actionable mitigation steps using a predefined security playbook.
* **Interactive Dashboard:** Upload events CSV or use sample data for instant insights.

---

## Data & Model

* **Input Data:** Event logs including IPs, severity, vulnerabilities, asset criticality, past incidents, authentication failures, malware alerts, and anomalous activity.
* **Machine Learning:** Uses **RandomForestClassifier** with preprocessing (encoding & imputation) to predict high-risk events.
* **Output:** Probability scores and recommended actions per event.

---

## Highlights

* Adjustable risk threshold for alerts
* Playbook-driven recommendations for rapid mitigation
* Ready for **real-time integration** with SIEM, EDR, or vulnerability scanning systems
* Designed for easy adoption by cybersecurity teams

---

## Future Enhancements

* Replace synthetic events with **live SIEM/EDR feeds**
* Add **real-time streaming** via Kafka or FastAPI
* Incorporate **financial impact analysis** and **what-if scenarios**
* Export insights to **Power BI, Tableau**, or integrate with **GRC tools**

---
