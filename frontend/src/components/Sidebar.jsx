const ITEMS = [
  { id: "dashboard", label: "📊 Dashboard" },
  { id: "upload", label: "📁 Upload Data" },
  { id: "simulate", label: "🔮 What-If Simulator" },
  { id: "chat", label: "💬 AI Business Chat" },
];

export default function Sidebar({ page, onNavigate }) {
  return (
    <nav className="flex w-56 flex-col gap-1 border-r bg-white p-4">
      {ITEMS.map((item) => (
        <button
          key={item.id}
          onClick={() => onNavigate(item.id)}
          className={`rounded-lg px-4 py-2 text-left text-sm font-medium transition ${
            page === item.id
              ? "bg-indigo-600 text-white"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          {item.label}
        </button>
      ))}
      <p className="mt-auto text-xs text-slate-400">
        BizTwin AI — Hackathon MVP
      </p>
    </nav>
  );
}
