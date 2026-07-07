import { useEffect, useState, Suspense, lazy } from "react";
import Sidebar from "./components/Sidebar.jsx";
import { getHealth } from "./api.js";
import ErrorBoundary from "./ErrorBoundary.jsx";

const Dashboard = lazy(() => import("./components/Dashboard.jsx"));
const UploadPage = lazy(() => import("./components/UploadPage.jsx"));
const SimulationPage = lazy(() => import("./components/SimulationPage.jsx"));
const ChatPanel = lazy(() => import("./components/ChatPanel.jsx"));

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [backendOk, setBackendOk] = useState(null);
  // Bump this to force the dashboard to refetch after a new upload
  const [dataVersion, setDataVersion] = useState(0);

  useEffect(() => {
    getHealth()
      .then(() => setBackendOk(true))
      .catch(() => setBackendOk(false));
  }, []);

  return (
    <div className="flex h-screen bg-slate-100 text-slate-800">
      <Sidebar page={page} onNavigate={setPage} />

      <div className="flex flex-1 flex-col overflow-hidden">
        <header className="flex items-center justify-between border-b bg-white px-6 py-4">
          <h1 className="text-xl font-bold">
            BizTwin <span className="text-indigo-600">AI</span>
          </h1>
          <span
            className={`rounded-full px-3 py-1 text-xs font-semibold ${
              backendOk === null
                ? "bg-slate-200 text-slate-600"
                : backendOk
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {backendOk === null
              ? "Checking backend…"
              : backendOk
              ? "● Backend connected"
              : "● Backend offline"}
          </span>
        </header>

        <main className="flex-1 overflow-y-auto p-6">
          <ErrorBoundary>
            <Suspense fallback={<div className="p-4">Loading…</div>}>
              {page === "dashboard" && <Dashboard dataVersion={dataVersion} />}
              {page === "upload" && (
                <UploadPage onUploaded={() => setDataVersion((v) => v + 1)} />
              )}
              {page === "simulate" && <SimulationPage />}
              {page === "chat" && <ChatPanel />}
            </Suspense>
          </ErrorBoundary>
        </main>
      </div>
    </div>
  );
}
