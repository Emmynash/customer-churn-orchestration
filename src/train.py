import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from datetime import datetime
import os

from src.preprocess import build_preprocessor
from src.config import FEATURES, TARGET, MODEL_VERSION, NUMERICAL_FEATURES, CATEGORICAL_FEATURES

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "telco_customer_churn_dataset.xlsx")
MODEL_DIR = os.path.join(BASE_DIR, "models")

def load_data(path):
    """Loads the dataset from the specified path."""
    df = pd.read_excel(DATA_PATH)

    #normalize column names
    df.columns = df.columns.str.strip()

    #Convert total_charges to numeric, coercing errors to NaN
    df["total_charges"] = pd.to_numeric(df["total_charges"], errors='coerce')

    #Basic data cleaning
    df = df.dropna() 

    #covert target variable to binary
    df[TARGET] = df[TARGET].map({'Yes': 1, 'No': 0})

    missing = [col for col in FEATURES if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in dataset: {missing}")

    return df


def train_model():

    df = load_data(DATA_PATH)
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
        )
    preprocessor = build_preprocessor(NUMERICAL_FEATURES, CATEGORICAL_FEATURES)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    pipeline.fit(X_train, y_train)

    # Evaluate the model
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    print(f"ROC AUC Score: {roc_auc_score(y_test, y_proba):.4f}")

    # Save the model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    model_path = os.path.join(MODEL_DIR, f"{MODEL_VERSION}_{timestamp}.joblib")

    joblib.dump(pipeline, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()

