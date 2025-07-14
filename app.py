
import streamlit as st
import pandas as pd
from geo_utils import filter_by_region_site_cell
from summary_utils import summarize_anomalies
from plot_utils import plot_labeled_anomalies
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Telecom Anomaly Detection Dashboard")

@st.cache_data
def load_and_merge(site_file, kpi_file):
    site_meta = pd.read_excel(site_file)
    df_labeled = pd.read_excel(kpi_file)
    df_labeled['begintime'] = pd.to_datetime(df_labeled['begintime'])
    merged = df_labeled.merge(
        site_meta[['Cell name', 'Region', 'District', 'Site Name', 'Latitude', 'Longitude']],
        left_on='Cell_Name', right_on='Cell name', how='left'
    )
    return merged

# File uploads
site_file = st.file_uploader("Upload Site Metadata (.xlsx)", type="xlsx")
kpi_file = st.file_uploader("Upload KPI Labeled Data (.xlsx)", type="xlsx")

if site_file and kpi_file:
    df_labeled = load_and_merge(site_file, kpi_file)

    st.sidebar.title("Filters")
    region = st.sidebar.selectbox("Select Region", [""] + sorted(df_labeled["Region"].dropna().unique()))
    site_options = df_labeled[df_labeled["Region"] == region]["Site Name"].dropna().unique() if region else df_labeled["Site Name"].dropna().unique()
    site_name = st.sidebar.selectbox("Select Site", [""] + sorted(site_options))
    cell_options = df_labeled[df_labeled["Site Name"] == site_name]["Cell_Name"].dropna().unique() if site_name else df_labeled["Cell_Name"].dropna().unique()
    cell_name = st.sidebar.selectbox("Select Cell", [""] + sorted(cell_options))
    freq_band = st.sidebar.selectbox("Frequency Band", ["", "L07", "L18", "L21"])

    filtered_df = filter_by_region_site_cell(
        df_labeled,
        region=region or None,
        site_name=site_name or None,
        cell_name=cell_name or None,
        freq_band=freq_band or None
    )

    st.subheader("Summary Report")
    if not filtered_df.empty:
        st.text(summarize_anomalies(filtered_df))
    else:
        st.warning("No data found with current filter.")

    st.subheader("Anomaly Plot")
    anomaly_cols = [col for col in filtered_df.columns if col.endswith("_anomaly_prophet")]
    if anomaly_cols:
        selected_kpi = st.selectbox("Select KPI to Plot", anomaly_cols)
        kpi_base = selected_kpi.replace("_anomaly_prophet", "")
        selected_cell = cell_name if cell_name else filtered_df["Cell_Name"].unique()[0]
        fig = plot_labeled_anomalies(filtered_df, selected_cell, kpi_base)
        if fig:
            st.pyplot(fig)
        else:
            st.warning("No data available to plot.")
    else:
        st.warning("No anomaly columns found in data.")

    st.subheader("Map View")
    map_df = filtered_df.dropna(subset=['Latitude', 'Longitude'])
    if not map_df.empty:
        map_center = [map_df["Latitude"].mean(), map_df["Longitude"].mean()]
        m = folium.Map(location=map_center, zoom_start=11)

        for _, row in map_df.iterrows():
            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                tooltip=row["Cell_Name"],
                popup=f"<b>Site:</b> {row['Site Name']}<br><b>Cell:</b> {row['Cell_Name']}",
                icon=folium.Icon(color="blue", icon="signal")
            ).add_to(m)
        st_folium(m, width=700, height=500)
    else:
        st.info("No mappable data with coordinates available.")
else:
    st.info("Please upload both site metadata and labeled KPI data.")
