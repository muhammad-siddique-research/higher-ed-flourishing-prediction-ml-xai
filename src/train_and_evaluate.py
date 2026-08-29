import os
import numpy as np
import pandas as pd
import shap
import matplotlib.pyplot as plt

from sklearn.model_selection import KFold, cross_validate
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import ElasticNetCV
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# 1. Feature Architecture Definition
NUMERIC_FEATURES = ["SCOMM", "INTEGRITY", "SPIR", "TUITION", "FIT"]
CATEGORICAL_FEATURES = ["FIRSTGEN", "GENDER", "FAMINCOME"]
TARGET = "TQ_MEAN"

def get_preprocessor():
    """Builds a scikit-learn preprocessing pipeline for numeric and categorical features."""
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False))
    ])
    return ColumnTransformer([
        ("num", num_pipe, NUMERIC_FEATURES),
        ("cat", cat_pipe, CATEGORICAL_FEATURES)
    ])

def run_benchmarks(df: pd.DataFrame):
    """Evaluates candidates using 10-fold cross-validation."""
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    models = {
        "ElasticNet (CV)": ElasticNetCV(cv=5, random_state=42),
        "Random Forest": RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=250, learning_rate=0.03, max_depth=4, random_state=42),
        "LightGBM Regressor": LGBMRegressor(n_estimators=250, learning_rate=0.03, max_depth=4, random_state=42, verbose=-1)
    }

    preprocessor = get_preprocessor()
    cv = KFold(n_splits=10, shuffle=True, random_state=42)
    results = []

    print("\n--- 10-Fold Cross-Validation Model Benchmark ---")
    for name, model in models.items():
        pipe = Pipeline([("prep", preprocessor), ("reg", model)])
        scores = cross_validate(pipe, X, y, cv=cv, scoring=["r2", "neg_root_mean_squared_error", "neg_mean_absolute_error"])
        
        r2_mean = np.mean(scores["test_r2"])
        rmse_mean = -np.mean(scores["test_neg_root_mean_squared_error"])
        mae_mean = -np.mean(scores["test_neg_mean_absolute_error"])
        
        results.append({"Model": name, "R2 (Mean)": r2_mean, "RMSE": rmse_mean, "MAE": mae_mean})
        print(f"{name:20s} | R² = {r2_mean:.4f} | RMSE = {rmse_mean:.4f} | MAE = {mae_mean:.4f}")

    return pd.DataFrame(results)

def run_shap_explanation(df: pd.DataFrame):
    """Computes Tree SHAP values and outputs feature attribution plots."""
    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET]

    preprocessor = get_preprocessor()
    X_trans = preprocessor.fit_transform(X)

    encoded_cats = list(preprocessor.named_transformers_["cat"].named_steps["encoder"].get_feature_names_out(CATEGORICAL_FEATURES))
    feature_names = NUMERIC_FEATURES + encoded_cats

    model = XGBRegressor(n_estimators=250, learning_rate=0.03, max_depth=4, random_state=42)
    model.fit(X_trans, y)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_trans)

    os.makedirs("figures", exist_ok=True)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_trans, feature_names=feature_names, show=False)
    plt.title("Tree SHAP Feature Attribution (Student Thriving)", fontsize=13, pad=15)
    plt.tight_layout()
    plt.savefig("figures/shap_summary_plot.png", dpi=300)
    plt.close()
    print("\n[SUCCESS] SHAP summary plot saved to 'figures/shap_summary_plot.png'")

if __name__ == "__main__":
    dataset_path = "data/raw/student_thriving_dataset.csv"
    if os.path.exists(dataset_path):
        data = pd.read_csv(dataset_path)
        run_benchmarks(data)
        run_shap_explanation(data)
    else:
        print(f"[INFO] Dataset not found at '{dataset_path}'. Please upload your CSV to execute locally.")
