import pandas as pd

def detect_anomalies(df: pd.DataFrame):
    # Accepts columns like: ['zone','value'] OR ['date','value']
    if 'value' not in df.columns:
        raise ValueError("CSV must contain 'value' column")

    vals = df['value']
    q1 = vals.quantile(0.25)
    q3 = vals.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    anomalies = []
    for idx, row in df.iterrows():
        v = row['value']
        label = row.get('zone', row.get('date', idx))
        if v < lower or v > upper:
            anomalies.append({
                "label": str(label),
                "value": float(v)
            })
    return anomalies