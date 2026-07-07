# business_twin.py
# ─────────────────────────────────────────────────────────────
# The Business Twin is a single in-memory object that holds the
# three DataFrames (sales, products, expenses) after they are
# uploaded.  Every other module (analytics, chat, simulate)
# reads from this object.  Nothing is written to disk.
# ─────────────────────────────────────────────────────────────

import pandas as pd
from pathlib import Path

# ── Paths to the bundled sample data ──────────────────────────
_SAMPLE_DIR = Path(__file__).parent / "sample_data"


class BusinessTwin:
    """
    Holds the three core DataFrames.

    Attributes
    ----------
    sales     : pd.DataFrame  – columns: date, product_id, quantity, unit_price
    products  : pd.DataFrame  – columns: product_id, product_name, cost_price, sale_price
    expenses  : pd.DataFrame  – columns: date, category, amount
    loaded    : bool          – True once real data has been uploaded
    """

    def __init__(self) -> None:
        self.sales: pd.DataFrame = pd.DataFrame()
        self.products: pd.DataFrame = pd.DataFrame()
        self.expenses: pd.DataFrame = pd.DataFrame()
        self.loaded: bool = False

    # ── loaders ───────────────────────────────────────────────

    def load_sample_data(self) -> None:
        """Load the bundled sample CSVs so the app is never empty."""
        self.sales = _read_sales(_SAMPLE_DIR / "sales.csv")
        self.products = _read_products(_SAMPLE_DIR / "products.csv")
        self.expenses = _read_expenses(_SAMPLE_DIR / "expenses.csv")
        self.loaded = True

    def load_from_bytes(
        self,
        sales_bytes: bytes | None = None,
        products_bytes: bytes | None = None,
        expenses_bytes: bytes | None = None,
    ) -> dict:
        """
        Replace one or more DataFrames with uploaded CSV bytes.
        Only replaces the files that were actually provided.
        Returns a summary dict: { filename: row_count }.
        """
        summary: dict = {}

        if sales_bytes is not None:
            import io
            self.sales = _read_sales(io.BytesIO(sales_bytes))
            summary["sales.csv"] = len(self.sales)

        if products_bytes is not None:
            import io
            self.products = _read_products(io.BytesIO(products_bytes))
            summary["products.csv"] = len(self.products)

        if expenses_bytes is not None:
            import io
            self.expenses = _read_expenses(io.BytesIO(expenses_bytes))
            summary["expenses.csv"] = len(self.expenses)

        if summary:
            self.loaded = True

        return summary

    # ── convenience getters ───────────────────────────────────

    def get_sales(self) -> pd.DataFrame:
        return self.sales

    def get_products(self) -> pd.DataFrame:
        return self.products

    def get_expenses(self) -> pd.DataFrame:
        return self.expenses

    def is_ready(self) -> bool:
        """True when all three DataFrames have at least one row."""
        return (
            not self.sales.empty
            and not self.products.empty
            and not self.expenses.empty
        )


# ── private helpers ────────────────────────────────────────────


def _read_sales(source) -> pd.DataFrame:
    """Read sales CSV and enforce expected dtypes."""
    df = pd.read_csv(source)
    # Normalise column names: strip whitespace, lowercase
    df.columns = [c.strip().lower() for c in df.columns]
    _require_columns(df, ["date", "product_id", "quantity", "unit_price"], "sales")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0)
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0)
    return df


def _read_products(source) -> pd.DataFrame:
    """Read products CSV and enforce expected dtypes."""
    df = pd.read_csv(source)
    df.columns = [c.strip().lower() for c in df.columns]
    _require_columns(
        df, ["product_id", "product_name", "cost_price", "sale_price"], "products"
    )
    df["cost_price"] = pd.to_numeric(df["cost_price"], errors="coerce").fillna(0)
    df["sale_price"] = pd.to_numeric(df["sale_price"], errors="coerce").fillna(0)
    return df


def _read_expenses(source) -> pd.DataFrame:
    """Read expenses CSV and enforce expected dtypes."""
    df = pd.read_csv(source)
    df.columns = [c.strip().lower() for c in df.columns]
    _require_columns(df, ["date", "category", "amount"], "expenses")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    return df


def _require_columns(df: pd.DataFrame, required: list, name: str) -> None:
    """Raise a clear ValueError if a required column is missing."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"{name}.csv is missing required columns: {missing}. "
            f"Found columns: {list(df.columns)}"
        )
