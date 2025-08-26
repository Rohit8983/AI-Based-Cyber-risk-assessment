import pandas as pd
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "sample_events.csv"
MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "risk_model.pkl"

def main():
    df = pd.read_csv(DATA_PATH)
    target = "label_high_risk"
    y = df[target].astype(int)
    X = df.drop(columns=[target, "timestamp", "src_ip", "dst_ip", "asset_id"])
    # Separate categorical and numeric features
    cat_cols = ["event_type", "severity"]
    num_cols = [c for c in X.columns if c not in cat_cols]
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
        ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]), num_cols)
    ])
    clf = RandomForestClassifier(
        n_estimators=250,
        max_depth=None,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced_subsample"
    )
    pipe = Pipeline([("pre", pre), ("clf", clf)])
    # Simple train/test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    pipe.fit(X_train, y_train)
    y_pred = pipe.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=False)
    print(report)
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    main()
