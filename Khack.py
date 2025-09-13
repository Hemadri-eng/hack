import os
import requests
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional

# ---------- Collect ----------
def download_file(url: str, local_path: Optional[str] = None) -> str:
    """Download CSV/JSON file from URL."""
    local = local_path or os.path.basename(url.split("?")[0]) or "ocean_data.csv"
    if not os.path.exists(local):
        print(f"Downloading {url} -> {local} ...")
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        with open(local, "wb") as f:
            f.write(resp.content)
    else:
        print(f"File already exists: {local}")
    return local

# ---------- Load ----------
def load_dataset(path: str) -> pd.DataFrame:
    """Load CSV or JSON dataset into pandas DataFrame."""
    if path.endswith(".csv"):
        return pd.read_csv(path)
    elif path.endswith(".json"):
        return pd.read_json(path)
    else:
        raise ValueError("Unsupported file format. Use CSV or JSON.")

# ---------- Clean ----------
def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic cleaning:
    - Remove duplicate rows
    - Handle missing values
    - Keep only numeric/ocean-related columns
    """
    df = df.drop_duplicates()

    # Drop columns that are completely empty
    df = df.dropna(axis=1, how="all")

    # Replace impossible values (like -9999) with NaN
    df = df.replace([-999, -9999, 9999], np.nan)

    # Convert TIME or date column if present
    for col in df.columns:
        if "time" in col.lower() or "date" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df

# ---------- Explain ----------
def dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate summary statistics for the dataset."""
    summary = {}
    summary["n_records"] = len(df)
    summary["columns"] = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            summary["columns"][col] = {
                "valid": df[col].count(),
                "min": float(df[col].min(skipna=True)),
                "max": float(df[col].max(skipna=True)),
                "mean": float(df[col].mean(skipna=True))
            }
    # Time coverage if available
    time_cols = [c for c in df.columns if "time" in c.lower() or "date" in c.lower()]
    if time_cols:
        summary["time_range"] = {
            "start": str(df[time_cols[0]].min()),
            "end": str(df[time_cols[0]].max())
        }
    return summary

def print_report(summary: Dict[str, Any]):
    print("\n=== Dataset Report ===")
    print(f"Total records: {summary['n_records']}")
    if "time_range" in summary:
        print(f"Time range: {summary['time_range']['start']} -> {summary['time_range']['end']}\n")
    for col, meta in summary["columns"].items():
        print(f" - {col}: valid={meta['valid']}, min={meta['min']}, max={meta['max']}, mean={meta['mean']}")

# ---------- Example Flow ----------
def example_flow(url: str):
    local = download_file(url)
    df = load_dataset(local)
    df_clean = clean_dataset(df)
    summary = dataset_summary(df_clean)
    print_report(summary)
    return df_clean, summary
if __name__ == "__main__":
    sample_url = "https://erddap.ucsd.edu/erddap/tabledap/argo_profile_index.csv?file,date_qc,platform_number,latitude,longitude&rows=100"

    try:
        df_clean, ds_summary = example_flow(sample_url)
    except Exception as ex:
        print("Example run failed (check URL). Error:", ex)
