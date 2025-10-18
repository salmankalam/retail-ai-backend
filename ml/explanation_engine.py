def explain_forecast(df):
    trend = df['y'].rolling(7).mean().iloc[-1] - df['y'].rolling(7).mean().iloc[-14]
    if trend > 0:
        return "Rising trend — possible holiday or seasonal effect"
    elif trend < 0:
        return "Falling trend — end of discount season"
    else:
        return "Stable demand pattern"
