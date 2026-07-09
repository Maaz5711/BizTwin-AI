# main.py
# ─────────────────────────────────────────────────────────────
# BizTwin AI  –  FastAPI backend
# Owner: Bilal (Backend Core & Data)
#
# Endpoints:
#   GET  /health     → { status: "ok" }
#   POST /upload     → accepts CSV files, returns row summary
#   GET  /analytics  → KPIs (wired to Maaz's analytics module)
#   POST /simulate   → what-if scenarios (wired to Maaz's module)
#   POST /chat       → AI chat (wired to Hamza's module)
# ─────────────────────────────────────────────────────────────

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from business_twin import BusinessTwin

# ── Load environment variables from .env ──────────────────────
load_dotenv()

# ── Create the FastAPI app ────────────────────────────────────
app = FastAPI(
    title="BizTwin AI",
    description="Backend API for the BizTwin AI business simulation platform.",
    version="0.1.0",
)

# ── CORS — allow the React frontend (port 5173) to call us ────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "http://127.0.0.1:3000",
     # Vercel frontend
        "https://YOUR-VERCEL-URL.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Single shared Business Twin instance ─────────────────────
# This object lives for the lifetime of the server process.
# All endpoints read/write through it.
twin = BusinessTwin()

# Pre-load sample data so the app is never empty on first run.
twin.load_sample_data()


@app.get("/", summary="Root endpoint")
def read_root() -> dict:
    return {
        "message": "BizTwin AI Backend is running!",
        "health_check": "/health",
        "docs": "/docs"
    }


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 1 — Health check
# GET /health
# ═══════════════════════════════════════════════════════════════


@app.get("/health", summary="Health check")
def health() -> dict:
    """
    Returns { status: 'ok' } when the server is running.
    The frontend calls this first to confirm the connection.
    """
    return {"status": "ok"}


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 2 — Upload CSV files
# POST /upload
# ═══════════════════════════════════════════════════════════════


@app.post("/upload", summary="Upload CSV files")
async def upload(
    sales: Optional[UploadFile] = File(None, description="sales.csv"),
    products: Optional[UploadFile] = File(None, description="products.csv"),
    expenses: Optional[UploadFile] = File(None, description="expenses.csv"),
) -> dict:
    """
    Accept one or more CSV files (sales, products, expenses).
    Each file is optional — only provided files replace the
    current in-memory data.  At least one file must be supplied.

    Returns a summary of how many rows were loaded per file.

    Example response:
    {
      "message": "Upload successful",
      "rows_loaded": {
        "sales.csv": 20,
        "products.csv": 8,
        "expenses.csv": 12
      }
    }
    """
    if sales is None and products is None and expenses is None:
        raise HTTPException(
            status_code=400,
            detail="No files were provided. Send at least one CSV file.",
        )

    # Read raw bytes from each uploaded file (if present)
    sales_bytes = await sales.read() if sales else None
    products_bytes = await products.read() if products else None
    expenses_bytes = await expenses.read() if expenses else None

    try:
        summary = twin.load_from_bytes(
            sales_bytes=sales_bytes,
            products_bytes=products_bytes,
            expenses_bytes=expenses_bytes,
        )
    except ValueError as exc:
        # load_from_bytes raises ValueError for bad columns
        raise HTTPException(status_code=422, detail=str(exc))

    return {"message": "Upload successful", "rows_loaded": summary}


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 3 — Analytics / KPIs
# GET /analytics
# ═══════════════════════════════════════════════════════════════


@app.get("/analytics", summary="Get KPIs and top products")
def analytics() -> dict:
    """
    Returns the core KPIs computed from the current Business Twin data:
      - revenue
      - expenses
      - profit
      - margin (as a percentage, 2 decimal places)
      - top_products (list of top 5 by revenue)

    This endpoint is owned by Maaz (analytics module).
    Bilal wires it here so Huzaifa can call it from the frontend.

    If Maaz's module is not yet ready, a safe fallback is used
    so the frontend always gets a valid response shape.
    """
    if not twin.is_ready:
        raise HTTPException(
            status_code=503,
            detail="No data loaded yet. Please upload CSV files first.",
        )

    # ── Try to import Maaz's analytics module ─────────────────
    # When Maaz's file exists, we use it.
    # Until then, the fallback below keeps everything working.
    try:
        from analytics import compute_analytics  # Maaz's module

        return compute_analytics(twin)

    except ImportError:
        # ── Fallback KPI calculation (Bilal's safe default) ───
        # Maaz will replace this logic with his own module.
        return _fallback_kpis(twin)


def _fallback_kpis(twin: BusinessTwin) -> dict:
    """
    Simple KPI calculation used until Maaz's analytics.py is ready.
    Maaz should NOT change this function — he should create analytics.py.
    """
    sales = twin.get_sales()
    products = twin.get_products()
    expenses = twin.get_expenses()

    # Revenue = sum(quantity × unit_price) for each sale row
    revenue = float((sales["quantity"] * sales["unit_price"]).sum())

    # Total expenses
    total_expenses = float(expenses["amount"].sum())

    # Profit
    profit = revenue - total_expenses

    # Margin (guard against divide-by-zero)
    margin = round((profit / revenue * 100), 2) if revenue > 0 else 0.0

    # Top 5 products by revenue
    # Join sales with products on product_id to get product names
    sales_with_name = sales.merge(products[["product_id", "product_name"]], on="product_id", how="left")
    sales_with_name["line_revenue"] = sales_with_name["quantity"] * sales_with_name["unit_price"]
    top = (
        sales_with_name.groupby("product_name")["line_revenue"]
        .sum()
        .nlargest(5)
        .reset_index()
        .rename(columns={"line_revenue": "revenue"})
    )
    top_products = top.to_dict(orient="records")

    return {
        "revenue": round(revenue, 2),
        "expenses": round(total_expenses, 2),
        "profit": round(profit, 2),
        "margin": margin,
        "top_products": top_products,
    }


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 4 — What-If Simulation
# POST /simulate
# ═══════════════════════════════════════════════════════════════


class SimulateRequest(BaseModel):
    scenario: str  # "supplier_price_increase" or "hire_salesperson"
    params: dict   # scenario-specific parameters


@app.post("/simulate", summary="Run a what-if simulation")
def simulate(body: SimulateRequest) -> dict:
    """
    Runs one of two what-if scenarios and returns before/after numbers.

    Scenarios:
      "supplier_price_increase"  – params: { increase_pct: float }
      "hire_salesperson"         – params: { salary: float, revenue_uplift_pct: float }

    This endpoint is owned by Maaz (simulation module).
    Bilal wires the route here.
    """
    if not twin.is_ready:
        raise HTTPException(
            status_code=503,
            detail="No data loaded yet. Please upload CSV files first.",
        )

    try:
        from simulations import run_simulation  # Maaz's module

        return run_simulation(twin, body.scenario, body.params)

    except ImportError:
        # Placeholder until Maaz's module is ready
        return {
            "scenario": body.scenario,
            "params": body.params,
            "note": "Simulation module not yet available. Maaz will implement simulations.py.",
        }
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ═══════════════════════════════════════════════════════════════
# ENDPOINT 5 — AI Chat
# POST /chat
# ═══════════════════════════════════════════════════════════════


class ChatRequest(BaseModel):
    question: str


@app.post("/chat", summary="Ask the AI a business question")
async def chat(body: ChatRequest) -> dict:
    """
    Takes a plain-English question and returns an AI answer
    grounded in the current business data.

    This endpoint is owned by Hamza (AI layer).
    Bilal wires the route here and passes the twin's current KPIs
    so Hamza's module always has fresh numbers to work with.
    """
    if not twin.is_ready:
        raise HTTPException(
            status_code=503,
            detail="No data loaded yet. Please upload CSV files first.",
        )

    if not body.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Build current KPI context to pass to Hamza's module
    try:
        from analytics import compute_analytics
        kpi_context = compute_analytics(twin)
    except ImportError:
        kpi_context = _fallback_kpis(twin)

    try:
        from ai_chat import answer_question  # Hamza's module
        response = answer_question(body.question, kpi_context)
        return {"answer": response}

    except ImportError:
        # Placeholder until Hamza's module is ready
        return {
            "answer": (
                f"[AI module not yet connected] "
                f"Based on your data: revenue is ${kpi_context['revenue']:,.2f}, "
                f"expenses are ${kpi_context['expenses']:,.2f}, "
                f"profit is ${kpi_context['profit']:,.2f}."
            )
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI service error: {exc}")
