const ITEMS = [
  { id: "dashboard", label: "📊 Dashboard" },
  { id: "upload", label: "📁 Upload Data" },
  { id: "simulate", label: "🔮 What-If Simulator" },
  { id: "chat", label: "💬 AI Business Chat" },
];

export default function Sidebar({ page, onNavigate }) {
  return (
    <nav className="flex h-full min-h-0 w-full flex-col gap-1 bg-white p-4 md:p-5">
      {ITEMS.map((item) => (
        <button
          key={item.id}
          onClick={() => onNavigate(item.id)}
          className={`rounded-lg px-4 py-2 text-left text-sm font-medium transition md:text-[15px] ${
            page === item.id
              ? "bg-indigo-600 text-white"
              : "text-slate-600 hover:bg-slate-100"
          }`}
        >
          {item.label}
        </button>
      ))}
      <p className="mt-auto pt-4 text-xs text-slate-400">
        BizTwin AI — Hackathon MVP
      </p>
    </nav>
  );
}
