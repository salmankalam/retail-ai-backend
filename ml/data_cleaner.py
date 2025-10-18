import pandas as pd
from sklearn.preprocessing import LabelEncoder

def clean_data(df: pd.DataFrame):
    summary = []
    df = df.copy()

    num_cols = df.select_dtypes(include=['float64','int64']).columns
    for col in num_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
            summary.append(f"Filled missing numeric values in '{col}'")

    cat_cols = df.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
            summary.append(f"Filled missing categorical values in '{col}'")

    for col in cat_cols:
        df[col] = LabelEncoder().fit_transform(df[col].astype(str))
        summary.append(f"Encoded categorical column '{col}'")

    for col in df.columns:
        if 'date' in col.lower():
            df[col] = pd.to_datetime(df[col], errors='coerce')
            summary.append(f"Converted '{col}' to datetime")

    return df, summary