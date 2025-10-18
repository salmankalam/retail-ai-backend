from prophet import Prophet
import pandas as pd
from ml.explanation_engine import explain_forecast

def predict_demand(df: pd.DataFrame, days: int = 7):
    predictions = []
    df['date'] = pd.to_datetime(df['date'])
    for sku in df['sku'].unique():
        sub = df[df['sku'] == sku][['date', 'sales']].rename(columns={'date': 'ds', 'sales': 'y'})
        model = Prophet(daily_seasonality=True)
        model.fit(sub)
        future = model.make_future_dataframe(periods=days)
        forecast = model.predict(future)
        future_forecast = forecast.tail(days)
        reason = explain_forecast(sub)
        predictions.append({
            "sku": sku,
            "predicted_sales": list(map(float, future_forecast['yhat'])),
            "reason": reason
        })
    return {"forecasts": predictions}