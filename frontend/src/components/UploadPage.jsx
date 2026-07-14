import { useState } from "react";
import { uploadFiles } from "../api.js";

const FILE_FIELDS = [
  { key: "sales", label: "sales.csv", hint: "date, product_id, quantity, unit_price" },
  { key: "products", label: "products.csv", hint: "product_id, product_name, cost_price, sale_price" },
  { key: "expenses", label: "expenses.csv", hint: "date, category, amount" },
];

export default function UploadPage({ onUploaded }) {
  const [files, setFiles] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setBusy(true);
    try {
      const res = await uploadFiles(files);
      setResult(res.loaded);
      onUploaded?.();
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="mx-auto w-full max-w-xl space-y-6">
      <div>
        <h2 className="text-lg font-bold sm:text-xl">Upload Your Business Data</h2>
        <p className="text-sm text-slate-500">
          Upload one or more CSV files. Sample data is pre-loaded, so this is optional for the demo.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-4 rounded-xl bg-white p-4 shadow-sm sm:p-6">
        {FILE_FIELDS.map(({ key, label, hint }) => (
          <div key={key}>
            <label className="block text-sm font-medium">{label}</label>
            <p className="mb-1 text-xs text-slate-400">Columns: {hint}</p>
            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFiles((f) => ({ ...f, [key]: e.target.files[0]}))}
              className="block w-full text-sm file:mr-3 file:rounded-lg file:border-0
                         file:bg-indigo-50 file:px-4 file:py-2 file:text-sm
                         file:font-semibold file:text-indigo-700 hover:file:bg-indigo-100"
            />
          </div>
        ))}

        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-lg bg-indigo-600 py-2 font-semibold text-white
                     transition hover:bg-indigo-700 disabled:opacity-50"
        >
          {busy ? "Uploading…" : "Upload"}
        </button>
      </form>

      {error && <p className="rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}

      {result && (
        <div className="rounded-lg bg-green-50 p-4 text-sm text-green-800">
          <p className="font-semibold">✅ Upload successful:</p>
          <ul className="mt-1 list-inside list-disc">
            {Object.entries(result).map(([name, rows]) => (
              <li key={name}>{name}: {rows} rows loaded</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
