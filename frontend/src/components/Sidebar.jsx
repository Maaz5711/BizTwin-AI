const ITEMS = [
  { id: "dashboard", label: "📊 Dashboard" },
  { id: "upload", label: "📁 Upload Data" },
  { id: "simulate", label: "🔮 What-If Simulator" },
  { id: "chat", label: "💬 AI Business Chat" },
];

export default function Sidebar({ page, onNavigate }) {
  return (
    <nav className="flex w-full shrink-0 flex-row gap-1 overflow-x-auto border-b bg-white p-3 md:w-56 md:flex-col md:overflow-visible md:border-b-0 md:border-r md:p-4">
      {ITEMS.map((item) => (
        <button
          key={item.id}
          onClick={() => onNavigate(item.id)}
          className={`shrink-0 rounded-lg px-4 py-2 text-left text-sm font-medium transition md:w-full ${
            page === item.id
              ? "bg-indigo-600 text-white"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          {item.label}
        </button>
      ))}
      <p className="ml-auto hidden text-xs text-slate-400 md:mt-auto md:ml-0 md:block">
        BizTwin AI — Hackathon MVP
      </p>
    </nav>
  );
}
