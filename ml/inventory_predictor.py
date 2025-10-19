import pandas as pd

def json_inventory_data(df: pd.DataFrame, days: int = None):
    # Ensure Date is datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date']).sort_values(by='Date')

    # Filter by most recent N days if specified
    if days is not None:
        latest_date = df['Date'].max()
        start_date = latest_date - pd.Timedelta(days=days)
        df = df[df['Date'] >= start_date]

    # Format Date and select columns (ignore if missing)
    expected_cols = ['Date', 'Inventory Level', 'OptimalInventory']
    available_cols = [col for col in expected_cols if col in df.columns]
    selected_df = df[available_cols].copy()

    # Convert Date to string for JSON
    if 'Date' in selected_df.columns:
        selected_df['Date'] = selected_df['Date'].dt.strftime('%Y-%m-%d')

    # Convert to JSON
    return selected_df.to_dict(orient='records')
