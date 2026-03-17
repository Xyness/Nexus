const colors: Record<string, string> = {
  pending: "bg-yellow-100 text-yellow-800 dark:bg-yellow-500/10 dark:text-yellow-400",
  running: "bg-blue-100 text-blue-800 dark:bg-blue-500/10 dark:text-blue-400",
  completed: "bg-green-100 text-green-800 dark:bg-green-500/10 dark:text-green-400",
  error: "bg-red-100 text-red-800 dark:bg-red-500/10 dark:text-red-400",
  bullish: "bg-green-100 text-green-800 dark:bg-green-500/10 dark:text-green-400",
  bearish: "bg-red-100 text-red-800 dark:bg-red-500/10 dark:text-red-400",
  neutral: "bg-gray-100 text-gray-800 dark:bg-zinc-700 dark:text-zinc-300",
};

export function Badge({ label }: { label: string }) {
  const color = colors[label.toLowerCase()] || "bg-gray-100 text-gray-700 dark:bg-zinc-700 dark:text-zinc-300";
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${color}`}>
      {label}
    </span>
  );
}
