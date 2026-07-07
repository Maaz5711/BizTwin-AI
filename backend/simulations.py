"""What-If simulations. Pure Python math — no AI, fully explainable."""
from analytics import compute_analytics


def run_simulation(twin, scenario: str, params: dict) -> dict:
    base = compute_analytics(twin)

    if scenario == "supplier_price_increase":
        pct = float(params.get("increase_pct", 10))
        new_cogs = base["cogs"] * (1 + pct / 100)
        new_profit = base["revenue"] - new_cogs - base["expenses"]
        explanation = (
            f"If supplier prices rise by {pct}%, cost of goods increases from "
            f"{base['cogs']:.2f} to {new_cogs:.2f}. Revenue and other expenses "
            f"stay the same, so profit changes from {base['profit']:.2f} to "
            f"{new_profit:.2f}."
        )
        after = _kpis(base["revenue"], new_cogs, base["expenses"])

    elif scenario == "hire_salesperson":
        salary = float(params.get("monthly_salary", 500))
        lift = float(params.get("revenue_increase_pct", 15))
        n_months = max(len({m["month"] for m in base["revenue_by_month"]}), 1)
        salary_total = salary * n_months
        new_revenue = base["revenue"] * (1 + lift / 100)
        # More sales means proportionally more cost of goods sold
        new_cogs = base["cogs"] * (1 + lift / 100)
        new_expenses = base["expenses"] + salary_total
        explanation = (
            f"Hiring a salesperson at {salary:.2f}/month over the {n_months}-month "
            f"data period adds {salary_total:.2f} in expenses. Assuming they lift "
            f"revenue by {lift}%, revenue grows from {base['revenue']:.2f} to "
            f"{new_revenue:.2f} (with proportional cost of goods). Profit moves "
            f"from {base['profit']:.2f} to "
            f"{new_revenue - new_cogs - new_expenses:.2f}."
        )
        after = _kpis(new_revenue, new_cogs, new_expenses)

    else:
        raise ValueError(f"Unknown scenario: {scenario}")

    before = _kpis(base["revenue"], base["cogs"], base["expenses"])
    delta = {k: round(after[k] - before[k], 2) for k in before}
    return {"scenario": scenario, "before": before, "after": after,
            "delta": delta, "explanation": explanation}


def _kpis(revenue: float, cogs: float, expenses: float) -> dict:
    profit = revenue - cogs - expenses
    margin = (profit / revenue * 100) if revenue else 0.0
    return {
        "revenue": round(revenue, 2),
        "cogs": round(cogs, 2),
        "expenses": round(expenses, 2),
        "profit": round(profit, 2),
        "margin": round(margin, 2),
    }
