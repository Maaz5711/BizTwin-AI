# BizTwin AI — API Contract

**Base URL (local):** `http://localhost:8000`  
**Auto-docs:** `http://localhost:8000/docs`

---

## Data Schema (CSV files)

| File | Columns |
|------|---------|
| sales.csv | date, product_id, quantity, unit_price |
| products.csv | product_id, product_name, cost_price, sale_price |
| expenses.csv | date, category, amount |

---

## Endpoints

### GET /health
Returns server status.  
**Response:** `{ "status": "ok" }`

---

### POST /upload
Accepts multipart/form-data with optional fields: `sales`, `products`, `expenses`.  
At least one file must be provided.

**Response:**

{
  "message": "Upload successful",
  "rows_loaded": {
    "sales.csv": 20,
    "products.csv": 5,
    "expenses.csv": 12
  }
}


---

### GET /analytics
Returns KPIs computed from the current Business Twin data.

**Response:**

{
  "revenue": 9240.50,
  "expenses": 9105.00,
  "profit": 135.50,
  "margin": 1.47,
  "top_products": [
    { "product_name": "USB-C Hub", "revenue": 2640.00 },
    { "product_name": "Mechanical Keyboard", "revenue": 1680.00 }
  ]
}

---

### POST /simulate
Runs a what-if simulation.

**Request body:**
{
  "scenario": "supplier_price_increase",
  "params": { "increase_pct": 10 }
}


**Response:** before/after numbers (implemented by Maaz).

---

### POST /chat
Asks the AI a business question.

**Request body:**
{ "question": "What is my profit margin?" }

**Response:**
{ "answer": "Your current profit margin is 1.47%..." }

---

## Notes for teammates

- **Maaz:** Create `backend/analytics.py` with a function `compute_kpis(twin) -> dict`.  
  Create `backend/simulations.py` with a function `run_simulation(twin, scenario, params) -> dict`.
- **Hamza:** Create `backend/ai_chat.py` with an async function `answer_question(question: str, kpi_context: dict) -> str`.
- **Huzaifa:** All endpoints return JSON. Use the response shapes above to build your UI with mock data first.
