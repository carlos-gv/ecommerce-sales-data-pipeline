# data/

This folder is intentionally empty in git. Running `lab1_data_engineering.ipynb` (top to bottom)
regenerates everything here:

| File | How it's produced |
|---|---|
| `1000_sales_records.csv` | Downloaded and unzipped automatically from the ExcelBIAnalytics source (`src/data_sources.py::ensure_raw_csv`) the first time the notebook runs. |
| `cleaned_transactions.csv` / `cleaned_transactions.json` | Written by the notebook's Step 11 (Serialization Checkpoint) after cleaning/transforming/feature-engineering the primary data. |

The secondary metadata source (product catalogue) is not a file at all — it's built in code by
`src/data_sources.py::build_product_catalog()` so the whole pipeline is reproducible from source with
no binary/data files tracked in git.

See the root [README.md](../README.md) for setup instructions.
