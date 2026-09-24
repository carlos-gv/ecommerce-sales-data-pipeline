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

Run all cells top-to-bottom; it writes `data/cleaned_transactions.csv` and `data/cleaned_transactions.json`.

## Data sources

- **Primary**: [ExcelBIAnalytics "1000 Sales Records"](https://excelbianalytics.com/wp/downloads-18-sample-csv-files-data-sets-for-testing-sales/) (`data/1000_sales_records.csv`) — first 500 rows used, augmented in-notebook with `customer_id`, `coupon_code`, and `shipping_city`, which the source file doesn't include.
- **Secondary**: `data/product_catalog.csv` — a hand-built product-category lookup covering the 12 `Item Type` values in the primary file, used to build the Data Dictionary and enrich features.

## Other projects

<!-- TODO: add up to 3 links to your other GitHub repos, e.g. -->
<!-- - [Project name](https://github.com/your-username/repo) -->

