import { useEffect, useState } from "react";
import Sidebar from "./components/Sidebar.jsx";
import Dashboard from "./components/Dashboard.jsx";
import UploadPage from "./components/UploadPage.jsx";
import SimulationPage from "./components/SimulationPage.jsx";
import ChatPanel from "./components/ChatPanel.jsx";
import { getHealth } from "./api.js";

export default function App() {
  const [page, setPage] = useState("dashboard");
  const [backendOk, setBackendOk] = useState(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  // Bump this to force the dashboard to refetch after a new upload
  const [dataVersion, setDataVersion] = useState(0);

  const navigateTo = (nextPage) => {
    setPage(nextPage);
    setMobileMenuOpen(false);
  };

  useEffect(() => {
    getHealth()
      .then(() => setBackendOk(true))
      .catch(() => setBackendOk(false));
  }, []);

  return (
    <div className="app-shell min-h-screen overflow-x-hidden bg-slate-100 text-slate-800">
      <aside className="app-sidebar-desktop fixed inset-y-0 left-0 z-30 hidden w-[220px] flex-col border-r border-slate-200 bg-white lg:w-64 md:flex">
        <Sidebar page={page} onNavigate={navigateTo} />
      </aside>

      {mobileMenuOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <button
            type="button"
            aria-label="Close menu"
            className="absolute inset-0 bg-slate-900/40"
            onClick={() => setMobileMenuOpen(false)}
          />
          <div className="mobile-drawer absolute inset-y-0 left-0 w-[min(18rem,85vw)] border-r border-slate-200 bg-white shadow-2xl">
            <Sidebar page={page} onNavigate={navigateTo} />
          </div>
        </div>
      )}

      <div className="flex min-h-screen min-w-0 flex-1 flex-col overflow-x-hidden md:pl-[220px] lg:pl-64">
        <header className="sticky top-0 z-20 flex items-center gap-3 border-b border-slate-200 bg-white/95 px-4 py-3 backdrop-blur sm:px-6">
          <button
            type="button"
            aria-label="Open menu"
            aria-expanded={mobileMenuOpen}
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-lg font-semibold text-slate-700 transition hover:bg-slate-100 md:hidden"
            onClick={() => setMobileMenuOpen(true)}
          >
            ☰
          </button>

          <h1 className="min-w-0 flex-1 truncate text-lg font-bold sm:text-xl">
            BizTwin <span className="text-indigo-600">AI</span>
          </h1>
          <span
            className={`shrink-0 rounded-full px-3 py-1 text-[11px] font-semibold sm:text-xs ${
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

        <main className="min-w-0 flex-1 overflow-x-hidden overflow-y-auto p-4 sm:p-6">
          {page === "dashboard" && <Dashboard dataVersion={dataVersion} />}
          {page === "upload" && (
            <UploadPage onUploaded={() => setDataVersion((v) => v + 1)} />
          )}
          {page === "simulate" && <SimulationPage />}
          {page === "chat" && <ChatPanel />}
        </main>
      </div>
    </div>
  );
}
