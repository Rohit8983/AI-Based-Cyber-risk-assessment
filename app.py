import streamlit as st
import pandas as pd
from pathlib import Path
import yaml
import plotly.express as px

# --- Page setup ---
st.set_page_config(page_title="AI-Based Real-Time Cyber Risk Assessment", layout="wide")
st.title("🔐 AI-Based Real-Time Cyber Risk Assessment")
st.caption("Upload events CSV → get risk probabilities, alerts, and mitigation recommendations.")

# --- Functions ---
def load_recommendations(cfg_path):
    """Load playbook and threshold from YAML config."""
    with open(cfg_path, "r") as f:
        config = yaml.safe_load(f)
    playbook = config.get("playbook", {})
    threshold = config.get("threshold", 0.5)
    return playbook, threshold

def score_events(df):
    """
    Scoring function: Add a 'risk_probability' column.
    Works with both event logs (severity, vuln_count) and networking logs (packet_size).
    """
    # Ensure severity exists
    if "severity" in df.columns:
        df["severity"] = pd.to_numeric(df["severity"], errors="coerce").fillna(1)
    else:
        df["severity"] = 1

    # Ensure vuln_count exists
    if "vuln_count" in df.columns:
        df["vuln_count"] = pd.to_numeric(df["vuln_count"], errors="coerce").fillna(0)
    else:
        df["vuln_count"] = 0

    # Ensure packet_size exists
    if "packet_size" in df.columns:
        df["packet_size"] = pd.to_numeric(df["packet_size"], errors="coerce").fillna(0)
    else:
        df["packet_size"] = 0

    # Risk calculation
    max_sev = df["severity"].max() or 10
    max_vuln = df["vuln_count"].max() or 1
    max_pkt = df["packet_size"].max() or 1

    df["risk_probability"] = (
        (df["severity"] / max_sev * 0.5) +
        (df["vuln_count"] / max_vuln * 0.3) +
        (df["packet_size"] / max_pkt * 0.2)
    )
    df["risk_probability"] = df["risk_probability"].clip(0, 1)

    return df

def suggest(playbook, event):
    """Return recommendations based on event_type or default advice."""
    event_type = event.get("event_type", "generic")
    return playbook.get(event_type, ["Investigate event", "Apply patch", "Isolate affected asset"])

# --- Load config ---
BASE = Path(__file__).resolve().parent
cfg_path = BASE / "config.yaml"
if not cfg_path.exists():
    sample_config = {
        "threshold": 0.5,
        "playbook": {
            "malware": ["Run antivirus scan", "Isolate infected machine", "Update malware signatures"],
            "phishing": ["Reset user passwords", "Block phishing domains", "Conduct user training"]
        }
    }
    with open(cfg_path, "w") as f:
        yaml.dump(sample_config, f)

playbook, threshold = load_recommendations(str(cfg_path))

# --- Sidebar settings ---
with st.sidebar:
    st.header("Settings")
    threshold = st.slider("Risk alert threshold", min_value=0.1, max_value=0.95,
                          value=float(threshold), step=0.05)
    st.write("Using recommendations from config.yaml.")

# --- Sample CSV download ---
sample_path = BASE / "data" / "sample_events.csv"
if not sample_path.exists():
    sample_path.parent.mkdir(parents=True, exist_ok=True)
    sample_csv = """event_type,severity,vuln_count,asset_criticality,asset_id
malware,7,3,8,asset_001
phishing,5,1,6,asset_002
dos,3,0,5,asset_003
ransomware,9,4,9,asset_004
malware,6,2,7,asset_005
"""
    with open(sample_path, "w") as f:
        f.write(sample_csv)

st.download_button("⬇️ Download sample_events.csv",
                   data=open(sample_path, "rb").read(),
                   file_name="sample_events.csv")

# --- File uploader ---
uploaded = st.file_uploader("Upload events CSV", type=["csv"])
if uploaded is None:
    st.info("Upload a CSV with columns like the sample or network logs.")
    df = pd.read_csv(sample_path).head(100)
    st.write("📂 Currently analyzing: sample_events.csv")
else:
    try:
        df = pd.read_csv(uploaded)
        st.success(f"📂 Currently analyzing: {uploaded.name}")
    except Exception as e:
        st.error(f"Error reading the uploaded CSV: {e}")
        st.stop()

# --- Scoring ---
scored = score_events(df.copy())
alerts = scored[scored["risk_probability"] >= threshold].copy()

# --- Determine dashboard title ---
if "packet_size" in scored.columns and "event_type" not in scored.columns:
    st.subheader("📡 Network Traffic Analysis")
else:
    st.subheader("📈 Scored Events")

st.dataframe(scored.head(200))

# --- Alerts ---
st.subheader("🚨 Alerts")
st.write(f"Threshold: {threshold:.2f} — Alerts: {len(alerts)}")
if alerts.empty:
    st.success("No alerts at the current threshold.")
else:
    for _, row in alerts.head(50).iterrows():
        with st.expander(
            f"ALERT • {row.get('event_type', 'N/A')} • asset={row.get('asset_id', row.get('src_ip', ''))} • risk={row['risk_probability']:.2f}"
        ):
            st.json(row.to_dict())
            recos = suggest(playbook, row.to_dict())
            st.markdown("Recommended actions:")
            for r in recos:
                st.markdown(f"- {r}")

# --- Radar Chart ---
st.subheader("📊 Radar (Polygon) Analysis")
numeric_cols = scored.select_dtypes(include="number").columns.tolist()
if len(numeric_cols) >= 3:
    radar_data = scored[numeric_cols].mean().reset_index()
    radar_data.columns = ["Metric", "Value"]
    fig = px.line_polar(radar_data, r="Value", theta="Metric", line_close=True)
    fig.update_traces(fill="toself")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Not enough numeric columns to generate a radar chart.")

# --- Download scored CSV ---
csv_bytes = scored.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download scored CSV", data=csv_bytes, file_name="scored_events.csv")
