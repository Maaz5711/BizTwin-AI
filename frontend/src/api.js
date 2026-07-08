// Single place for all backend calls — matches docs/API_CONTRACT.md
const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function handle(res) {
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed (${res.status})`);
  }
  return res.json();
}

export function getHealth() {
  return fetch(`${BASE_URL}/health`).then(handle);
}

export function uploadFiles({ sales, products, expenses }) {
  const form = new FormData();
  if (sales) form.append("sales", sales);
  if (products) form.append("products", products);
  if (expenses) form.append("expenses", expenses);
  return fetch(`${BASE_URL}/upload`, { method: "POST", body: form }).then(handle);
}

export function getAnalytics() {
  return fetch(`${BASE_URL}/analytics`).then(handle);
}

export function runSimulation(scenario, params) {
  return fetch(`${BASE_URL}/simulate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ scenario, params }),
  }).then(handle);
}

export function askChat(question) {
  return fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  }).then(handle);
}
