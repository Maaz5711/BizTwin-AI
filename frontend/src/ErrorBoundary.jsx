import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    // Log to console; in production send to monitoring
    console.error("ErrorBoundary caught an error:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-6">
          <h2 className="text-red-600 font-bold">Something went wrong.</h2>
          <pre className="whitespace-pre-wrap text-sm text-slate-700">{String(this.state.error)}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}
