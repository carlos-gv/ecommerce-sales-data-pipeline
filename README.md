# Lab 1 — Data Collection and Pre-Processing

An end-to-end Data Engineering walkthrough (ingest → wrangle → clean → transform → feature-engineer →
serialize) on a 500-row e-commerce sales dataset. The notebook loads a real public sales CSV, augments it
with the fields the assignment requires, cleans deliberately-injected data-quality issues, engineers a few
features, and serializes the result to CSV and JSON. Built for the MLProgramming-1 Data Collection and
Pre-Processing lab.

## Quick-start

```bash
python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows
pip install -r requirements.txt
jupyter notebook lab1_data_engineering.ipynb
```

No data files are committed to this repo — `data/` is empty except for a placeholder README. Running all
cells top-to-bottom downloads the primary CSV automatically, builds the secondary catalogue in code, and
writes `data/cleaned_transactions.csv` and `data/cleaned_transactions.json` as the final serialized output.
See `data/README.md` for exactly what lands where.

## Data sources

- **Primary**: [ExcelBIAnalytics "1000 Sales Records"](https://excelbianalytics.com/wp/downloads-18-sample-csv-files-data-sets-for-testing-sales/) — downloaded and unzipped automatically by `src/data_sources.py::ensure_raw_csv` the first time the notebook runs; first 500 rows are used, augmented in-notebook with `customer_id`, `coupon_code`, and `shipping_city`, which the source file doesn't include.
- **Secondary**: a product-category lookup covering the 12 `Item Type` values in the primary file, built in code by `src/data_sources.py::build_product_catalog` (no file to download) — used to build the Data Dictionary and enrich features.

## Other projects

<!-- TODO: add up to 3 links to your other GitHub repos, e.g. -->
<!-- - [Project name](https://github.com/your-username/repo) -->

