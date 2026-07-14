import { useState, useRef, useEffect } from "react";
import { askChat } from "../api.js";

const SUGGESTIONS = [
  "What is my profit?",
  "Which product makes the most money?",
  "How much am I spending on expenses?",
];

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    { role: "ai", text: "Hi! I'm BizTwin, your AI business analyst. Ask me anything about your numbers." },
  ]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async (question) => {
    const q = (question ?? input).trim();
    if (!q || busy) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", text: q }]);
    setBusy(true);
    try {
      const { answer } = await askChat(q);
      setMessages((m) => [...m, { role: "ai", text: answer }]);
    } catch (e) {
      setMessages((m) => [...m, { role: "ai", text: `Sorry, something went wrong: ${e.message}` }]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="flex h-full min-h-0 w-full min-w-0 flex-col">
      <div className="flex-1 space-y-3 overflow-y-auto rounded-2xl bg-white p-4 shadow-sm sm:p-5">
        {messages.map((m, i) => (
          <div key={i} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[90%] whitespace-pre-wrap rounded-2xl px-4 py-2 text-sm sm:max-w-[80%] ${
                m.role === "user"
                  ? "bg-indigo-600 text-white"
                  : "bg-slate-100 text-slate-800"
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
        {busy && <p className="text-sm text-slate-400">BizTwin is thinking…</p>}
        <div ref={bottomRef} />
      </div>

      <div className="mt-3 flex flex-wrap gap-2">
        {SUGGESTIONS.map((s) => (
          <button
            key={s}
            onClick={() => send(s)}
            className="rounded-full border border-indigo-200 bg-indigo-50 px-3 py-1
                       text-[11px] text-indigo-700 transition hover:bg-indigo-100 sm:text-xs"
          >
            {s}
          </button>
        ))}
      </div>

      <form
        onSubmit={(e) => { e.preventDefault(); send(); }}
        className="mt-3 flex flex-col gap-2 sm:flex-row"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your business…"
          className="min-w-0 flex-1 rounded-lg border border-slate-300 px-4 py-2 text-sm
                     focus:border-indigo-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={busy}
          className="w-full rounded-lg bg-indigo-600 px-5 py-2 font-semibold text-white
                     sm:w-auto
                     transition hover:bg-indigo-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}
