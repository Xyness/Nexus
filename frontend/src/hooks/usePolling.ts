"use client";

import { useEffect, useRef, useState } from "react";

export function usePolling<T>(
  fetcher: () => Promise<T>,
  intervalMs: number = 5000
) {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    let mounted = true;

    const poll = async () => {
      try {
        const result = await fetcher();
        if (mounted) {
          setData(result);
          setError(null);
          setLoading(false);
        }
      } catch (e) {
        if (mounted) {
          setError(e instanceof Error ? e.message : "Unknown error");
          setLoading(false);
        }
      }
    };

    poll();
    intervalRef.current = setInterval(poll, intervalMs);

    return () => {
      mounted = false;
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [fetcher, intervalMs]);

  const refresh = async () => {
    try {
      const result = await fetcher();
      setData(result);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    }
  };

  return { data, error, loading, refresh };
}
