import pandas as pd
import numpy as np

def analyze_data(df: pd.DataFrame):
    issues, recommendations = [], []
    score = 100

    missing = df.isnull().mean() * 100
    for col, pct in missing.items():
        if pct > 0:
            issues.append(f"{col}: {pct:.1f}% missing values")
            recommendations.append(f"Impute missing values in '{col}'")
            score -= min(pct, 20)

    for col in df.columns:
        if df[col].dtype == 'object' and df[col].nunique() > len(df) * 0.8:
            issues.append(f"{col}: possibly incorrect data type (too many unique values)")
            score -= 5

    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        zscore = ((df[col] - df[col].mean()) / df[col].std()).abs()
        if (zscore > 3).sum() > 0:
            issues.append(f"Outliers detected in {col}")
            recommendations.append(f"Review outliers in '{col}'")

    score = max(score, 0)
    return {
        "data_quality_score": round(score, 2),
        "issues": issues,
        "recommendations": recommendations
    }