import { useEffect, useState } from "react";
import {
  BarChart, Bar, LineChart, Line, XAxis, YAxis,
  Tooltip, ResponsiveContainer, CartesianGrid,
} from "recharts";
import { getAnalytics } from "../api.js";

const money = (n) =>
  n?.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });

function KpiCard({ label, value, accent }) {
  return (
    <div className="min-w-0 rounded-2xl bg-white p-4 shadow-sm sm:p-5">
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500 sm:text-sm">
        {label}
      </p>
      <p className={`mt-1 text-xl font-bold sm:text-2xl ${accent}`}>{value}</p>
    </div>
  );
}

export default function Dashboard({ dataVersion }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getAnalytics().then(setData).catch((e) => setError(e.message));
  }, [dataVersion]);

  if (error) return <p className="text-red-600">Error: {error}</p>;
  if (!data) return <p className="text-slate-500">Loading analytics…</p>;

  return (
    <div className="min-w-0 space-y-6">
      {/* KPI cards */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <KpiCard label="Revenue" value={money(data.revenue)} accent="text-indigo-600" />
        <KpiCard
          label="Profit"
          value={money(data.profit)}
          accent={data.profit >= 0 ? "text-green-600" : "text-red-600"}
        />
        <KpiCard label="Expenses" value={money(data.expenses)} accent="text-orange-500" />
        <KpiCard label="Margin" value={`${data.margin}%`} accent="text-purple-600" />
      </div>

      {/* Charts */}
      <div className="grid gap-6 lg:grid-cols-2">
        <div className="min-w-0 rounded-2xl bg-white p-4 shadow-sm sm:p-5">
          <h2 className="mb-4 text-sm font-semibold sm:text-base">Revenue by Month</h2>
          <div className="h-64 w-full sm:h-72 lg:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={data.revenue_by_month}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" fontSize={12} />
                <YAxis fontSize={12} />
                <Tooltip formatter={(v) => money(v)} />
                <Line type="monotone" dataKey="revenue" stroke="#4f46e5" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="min-w-0 rounded-2xl bg-white p-4 shadow-sm sm:p-5">
          <h2 className="mb-4 text-sm font-semibold sm:text-base">Top 5 Products by Revenue</h2>
          <div className="h-64 w-full sm:h-72 lg:h-80">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.top_products}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="product_name" fontSize={11} interval={0} angle={-15} dy={8} />
                <YAxis fontSize={12} />
                <Tooltip formatter={(v) => money(v)} />
                <Bar dataKey="total_revenue" fill="#4f46e5" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
