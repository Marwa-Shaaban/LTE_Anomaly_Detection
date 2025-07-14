
import matplotlib.pyplot as plt
import pandas as pd

def plot_labeled_anomalies(df, cell_name, kpi):
    df = df[df["Cell_Name"] == cell_name].copy()
    if df.empty or kpi not in df.columns or f"{kpi}_anomaly_prophet" not in df.columns:
        return None

    df["begintime"] = pd.to_datetime(df["begintime"])
    df = df.sort_values("begintime")
    anomalies = df[df[f"{kpi}_anomaly_prophet"] == 1]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df["begintime"], df[kpi], label="Actual", color="blue")
    ax.scatter(anomalies["begintime"], anomalies[kpi], color="red", label="Anomaly", zorder=5)
    ax.set_title(f"{kpi} - {cell_name}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
