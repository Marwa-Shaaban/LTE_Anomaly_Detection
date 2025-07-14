
def filter_by_region_site_cell(df, region=None, site_name=None, cell_name=None, freq_band=None):
    filtered = df.copy()
    if region:
        filtered = filtered[filtered["Region"] == region]
    if site_name:
        filtered = filtered[filtered["Site Name"] == site_name]
    if cell_name:
        filtered = filtered[filtered["Cell_Name"] == cell_name]
    if freq_band:
        filtered = filtered[filtered["Cell_Name"].str.startswith(freq_band)]
    return filtered
