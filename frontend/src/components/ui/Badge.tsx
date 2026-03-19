const colors: Record<string, string> = {
  // Status
  pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-500/10 dark:text-yellow-400",
  running: "bg-blue-100 text-blue-800 dark:bg-blue-500/10 dark:text-blue-400",
  completed: "bg-green-100 text-green-800 dark:bg-green-500/10 dark:text-green-400",
  error: "bg-red-100 text-red-800 dark:bg-red-500/10 dark:text-red-400",
  // Sentiment
  bullish: "bg-green-100 text-green-800 dark:bg-green-500/10 dark:text-green-400",
  bearish: "bg-red-100 text-red-800 dark:bg-red-500/10 dark:text-red-400",
  neutral: "bg-gray-100 text-gray-800 dark:bg-zinc-700 dark:text-zinc-300",
  // Urgency
  breaking: "bg-red-200 text-red-900 dark:bg-red-500/20 dark:text-red-300 font-semibold",
  important: "bg-orange-100 text-orange-800 dark:bg-orange-500/15 dark:text-orange-400",
  normal: "bg-blue-50 text-blue-700 dark:bg-blue-500/10 dark:text-blue-400",
  noise: "bg-gray-100 text-gray-500 dark:bg-zinc-800 dark:text-zinc-500",
};

export function Badge({ label }: { label: string }) {
  const color = colors[label.toLowerCase()] || "bg-gray-100 text-gray-700 dark:bg-zinc-700 dark:text-zinc-300";
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
      {label}
    </span>
  );
}
