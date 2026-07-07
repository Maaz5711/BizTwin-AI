# business_twin.py
# ─────────────────────────────────────────────────────────────
# The Business Twin is a single in-memory object that holds the
# three DataFrames (sales, products, expenses) after they are
# uploaded.  Every other module (analytics, chat, simulate)
# reads from this object.  Nothing is written to disk.
# ─────────────────────────────────────────────────────────────

"""The Business Twin: one in-memory object holding all business data."""
import io
from pathlib import Path
import pandas as pd

SAMPLE_DIR = Path(__file__).parent / "sample_data"

REQUIRED_COLUMNS = {
    "sales": ["date", "product_id", "quantity", "unit_price"],
    "products": ["product_id", "product_name", "cost_price", "sale_price"],
    "expenses": ["date", "category", "amount"],
}


class BusinessTwin:
    def __init__(self):
        self.data: dict[str, pd.DataFrame] = {}

    def load_sample_data(self) -> None:
        """Load bundled CSVs so the app is never empty."""
        for name in REQUIRED_COLUMNS:
            path = SAMPLE_DIR / f"{name}.csv"
            if path.exists():
                self.data[name] = self._clean(name, pd.read_csv(path))

    def load_csv_bytes(self, name: str, content: bytes) -> int:
        """Load an uploaded CSV. Returns number of rows loaded."""
        df = pd.read_csv(io.BytesIO(content))
        missing = set(REQUIRED_COLUMNS[name]) - set(df.columns)
        if missing:
            raise ValueError(f"{name}.csv is missing columns: {sorted(missing)}")
        self.data[name] = self._clean(name, df)
        return len(self.data[name])

    @staticmethod
    def _clean(name: str, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(subset=REQUIRED_COLUMNS[name]).copy()
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.dropna(subset=["date"])
        for col in ("quantity", "unit_price", "cost_price", "sale_price", "amount"):
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df.dropna()

    @property
    def is_ready(self) -> bool:
        return all(k in self.data for k in REQUIRED_COLUMNS)


# Singleton shared across the whole app
twin = BusinessTwin()
