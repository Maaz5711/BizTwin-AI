import { useState } from "react";
import { runSimulation } from "../api.js";

const money = (n) =>
  n?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const KPI_ROWS = ["revenue", "cogs", "expenses", "profit", "margin"];

export default function SimulationPage() {
  const [scenario, setScenario] = useState("supplier_price_increase");
  const [increasePct, setIncreasePct] = useState(10);
  const [salary, setSalary] = useState(500);
  const [lift, setLift] = useState(15);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const run = async () => {
    setError("");
    setBusy(true);
    try {
      const params =
        scenario === "supplier_price_increase"
          ? { increase_pct: Number(increasePct) }
          : { monthly_salary: Number(salary), revenue_increase_pct: Number(lift) };
      setResult(await runSimulation(scenario, params));
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-3xl space-y-6">
      <div>
        <h2 className="text-lg font-bold sm:text-xl">What-If Simulator</h2>
        <p className="text-sm text-slate-500">
          Pure math on your real data — every number is explainable.
        </p>
      </div>

      <div className="space-y-4 rounded-xl bg-white p-4 shadow-sm sm:p-6">
        <div>
          <label className="block text-sm font-medium">Scenario</label>
          <select
            value={scenario}
            onChange={(e) => { setScenario(e.target.value); setResult(null); }}
            className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm"
          >
            <option value="supplier_price_increase">Supplier price increase</option>
            <option value="hire_salesperson">Hire a salesperson</option>
          </select>
        </div>

        {scenario === "supplier_price_increase" ? (
          <div>
            <label className="block text-sm font-medium">Price increase (%)</label>
            <input
              type="number" value={increasePct}
              onChange={(e) => setIncreasePct(e.target.value)}
              className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm"
            />
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium">Monthly salary</label>
              <input
                type="number" value={salary}
                onChange={(e) => setSalary(e.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium">Revenue lift (%)</label>
              <input
                type="number" value={lift}
                onChange={(e) => setLift(e.target.value)}
                className="mt-1 w-full rounded-lg border border-slate-300 p-2 text-sm"
              />
            </div>
          </div>
        )}

        <button
          onClick={run}
          disabled={busy}
          className="w-full rounded-lg bg-indigo-600 px-6 py-2 font-semibold text-white sm:w-auto
                     transition hover:bg-indigo-700 disabled:opacity-50"
        >
          {busy ? "Running…" : "Run Simulation"}
        </button>
      </div>

      {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      {result && (
        <div className="space-y-4 rounded-xl bg-white p-4 shadow-sm sm:p-6">
          <h3 className="font-semibold">Results</h3>
          <div className="overflow-x-auto">
            <table className="min-w-[640px] w-full text-sm">
              <thead>
                <tr className="border-b text-left text-slate-500">
                  <th className="py-2">KPI</th>
                  <th>Before</th>
                  <th>After</th>
                  <th>Change</th>
                </tr>
              </thead>
              <tbody>
                {KPI_ROWS.map((k) => (
                  <tr key={k} className="border-b last:border-0">
                    <td className="py-2 font-medium capitalize">{k}</td>
                    <td>{k === "margin" ? `${result.before[k]}%` : money(result.before[k])}</td>
                    <td>{k === "margin" ? `${result.after[k]}%` : money(result.after[k])}</td>
                    <td className={result.delta[k] >= 0 ? "text-green-600" : "text-red-600"}>
                      {result.delta[k] >= 0 ? "+" : ""}
                      {k === "margin" ? `${result.delta[k]}%` : money(result.delta[k])}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="rounded-lg bg-indigo-50 p-4 text-sm text-indigo-900">
            <span className="font-semibold">Explanation: </span>
            {result.explanation}
          </p>
        </div>
      )}
    </div>
  );
}
