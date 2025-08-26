from pathlib import Path
import joblib
import pandas as pd

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "risk_model.pkl"

_model = None
def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

def score_events(df: pd.DataFrame):
    model = load_model()
    # Align features used in training
    to_drop = ["timestamp", "src_ip", "dst_ip", "asset_id", "label_high_risk"]
    cols = [c for c in df.columns if c not in to_drop]
    X = df[cols].copy()
    proba = model.predict_proba(X)[:,1]
    preds = (proba >= 0.5).astype(int)
    out = df.copy()
    out["risk_probability"] = proba
    out["risk_label"] = preds
    return out
