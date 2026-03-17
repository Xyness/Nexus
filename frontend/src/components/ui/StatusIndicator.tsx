import { Spinner } from "./Spinner";
import { Badge } from "./Badge";

export function StatusIndicator({ status }: { status: string }) {
  if (status === "running") {
    return (
      <span className="inline-flex items-center gap-1.5">
        <Spinner size="sm" />
        <span className="text-sm text-blue-700 dark:text-blue-400">Analyzing...</span>
      </span>
    );
  }
  return <Badge label={status} />;
}
