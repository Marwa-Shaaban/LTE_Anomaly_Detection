
def summarize_anomalies(df):
    summary = []
    total_cells = df["Cell_Name"].nunique()
    summary.append(f"📶 Total Cells Analyzed: {total_cells}")

    anomaly_cols = [col for col in df.columns if col.endswith("_anomaly_prophet")]
    if not anomaly_cols:
        return "No anomaly columns found in the data."

    for col in anomaly_cols:
        count = df[col].sum()
        kpi_name = col.replace("_anomaly_prophet", "")
        summary.append(f"🔍 {kpi_name}: {count} anomalies")

    most_affected = df[anomaly_cols].sum().sort_values(ascending=False)
    top_kpi = most_affected.index[0].replace("_anomaly_prophet", "") if not most_affected.empty else "None"
    summary.append(f"📈 Most Affected KPI: {top_kpi}")

    return "\n".join(summary)
