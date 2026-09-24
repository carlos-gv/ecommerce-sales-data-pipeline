"""Data acquisition for the lab: fetches the primary CSV and builds the secondary catalogue in code.

No data files are committed to the repo. Running the notebook (or this module directly) regenerates
everything into data/, which is git-ignored.
"""

import io
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

PRIMARY_SOURCE_URL = "https://excelbianalytics.com/wp/wp-content/uploads/2017/07/1000-Sales-Records.zip"
PRIMARY_SOURCE_PAGE = "https://excelbianalytics.com/downloads-18-sample-csv-files-data-sets-for-testing-sales/"
MAX_ATTEMPTS = 2


def ensure_raw_csv(dest: Path) -> Path:
    """Download and unzip the primary ExcelBIAnalytics sales CSV to `dest` if it isn't already there.

    Retries up to MAX_ATTEMPTS times; if every attempt fails, raises with instructions for a manual
    download instead of leaving the notebook stuck on an opaque network error.
    """
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    # The host rejects requests with Python's default urllib User-Agent (HTTP 406), so use a browser-like one.
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
    }
    request = urllib.request.Request(PRIMARY_SOURCE_URL, headers=headers)

    last_error = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as resp:
                zip_bytes = resp.read()
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                csv_name = next(n for n in zf.namelist() if n.lower().endswith(".csv"))
                with zf.open(csv_name) as src:
                    dest.write_bytes(src.read())
            return dest
        except (urllib.error.URLError, zipfile.BadZipFile, StopIteration, TimeoutError) as exc:
            last_error = exc
            if attempt < MAX_ATTEMPTS:
                time.sleep(2)

    raise RuntimeError(
        f"Could not download the primary dataset automatically after {MAX_ATTEMPTS} attempts "
        f"(last error: {last_error}).\n\n"
        "Please download it manually:\n"
        f"  1. Go to {PRIMARY_SOURCE_PAGE}\n"
        '  2. Find and download the "1000 Sales Record" CSV file\n'
        f"  3. Save/rename it to {dest}\n"
        "  4. Re-run this cell."
    )


# Secondary metadata source: a product catalogue covering the 12 `Item Type` values found in the
# primary file. Kept as code (not a committed CSV) so the whole repo is reproducible from source.
_PRODUCT_CATALOG_ROWS = [
    ("Baby Food", "Household & Family", True, 270,
     "Prepared or formulated food products intended for infants and toddlers."),
    ("Beverages", "Food & Grocery", True, 180,
     "Non-alcoholic drinks including juices, soft drinks, and bottled water."),
    ("Cereal", "Food & Grocery", False, 365,
     "Breakfast grain products such as cornflakes, oats, and granola."),
    ("Clothes", "Apparel", False, 1825,
     "Ready-to-wear garments and textile accessories for adults and children."),
    ("Cosmetics", "Personal Care", False, 730,
     "Skincare, makeup, and grooming products for personal use."),
    ("Fruits", "Food & Grocery", True, 14,
     "Fresh whole fruits sold by weight or unit."),
    ("Household", "Home Goods", False, 3650,
     "Cleaning supplies, kitchenware, and general home-maintenance items."),
    ("Meat", "Food & Grocery", True, 10,
     "Fresh or frozen animal protein products including beef, poultry, and pork."),
    ("Office Supplies", "Business & Office", False, 3650,
     "Stationery and administrative supplies such as paper, pens, and folders."),
    ("Personal Care", "Personal Care", False, 730,
     "Hygiene products including soap, shampoo, and oral care items."),
    ("Snacks", "Food & Grocery", False, 270,
     "Packaged snack foods such as chips, crackers, and cookies."),
    ("Vegetables", "Food & Grocery", True, 14,
     "Fresh whole vegetables sold by weight or unit."),
]

_CATALOG_COLUMNS = ["product", "category", "is_perishable", "shelf_life_days", "description"]


def build_product_catalog() -> pd.DataFrame:
    """Secondary metadata source: product -> category/perishability/description lookup."""
    return pd.DataFrame(_PRODUCT_CATALOG_ROWS, columns=_CATALOG_COLUMNS)
