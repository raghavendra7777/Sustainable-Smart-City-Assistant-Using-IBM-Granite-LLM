import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def fit_linear_forecast(df: pd.DataFrame, horizon: int = 12):
    # Expect columns: 'date' or 'period', and 'value'
    if 'value' not in df.columns:
        raise ValueError("CSV must contain 'value' column")
    if 'date' in df.columns:
        df['t'] = pd.to_datetime(df['date'])
        df = df.sort_values('t')
        df['x'] = np.arange(len(df))
    elif 'period' in df.columns:
        df = df.sort_values('period')
        df['x'] = np.arange(len(df))
    else:
        raise ValueError("CSV must contain either 'date' or 'period' column")

    X = df[['x']].values
    y = df['value'].values
    model = LinearRegression().fit(X, y)
    last_x = df['x'].iloc[-1]
    future_x = np.arange(last_x + 1, last_x + 1 + horizon).reshape(-1, 1)
    preds = model.predict(future_x)
    return preds.tolist()