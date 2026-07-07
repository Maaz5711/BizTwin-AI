"""KPI calculations. All numbers come straight from the data."""
import pandas as pd


def compute_analytics(twin) -> dict:
    sales = twin.data["sales"]
    products = twin.data["products"]
    expenses = twin.data["expenses"]

    merged = sales.merge(products, on="product_id", how="left")
    merged["revenue"] = merged["quantity"] * merged["unit_price"]
    merged["cogs"] = merged["quantity"] * merged["cost_price"]

    revenue = float(merged["revenue"].sum())
    cogs = float(merged["cogs"].sum())
    total_expenses = float(expenses["amount"].sum())
    profit = revenue - cogs - total_expenses
    margin = (profit / revenue * 100) if revenue else 0.0

    top_products = (
        merged.groupby("product_name")["revenue"].sum()
        .sort_values(ascending=False).head(5)
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
        .to_dict(orient="records")
    )

    revenue_by_month = (
        merged.assign(month=merged["date"].dt.strftime("%Y-%m"))
        .groupby("month")["revenue"].sum()
        .reset_index()
        .to_dict(orient="records")
    )

    expenses_by_category = (
        expenses.groupby("category")["amount"].sum()
        .reset_index()
        .to_dict(orient="records")
    )

    return {
        "revenue": round(revenue, 2),
        "cogs": round(cogs, 2),
        "expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "margin": round(margin, 2),
        "top_products": top_products,
        "revenue_by_month": revenue_by_month,
        "expenses_by_category": expenses_by_category,
    }
