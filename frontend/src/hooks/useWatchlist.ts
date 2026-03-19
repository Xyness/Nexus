"use client";

import { useCallback } from "react";
import { usePolling } from "./usePolling";
import { api } from "@/lib/api";

export function useWatchlist() {
  const fetcher = useCallback(() => api.getWatchlist(), []);
  return usePolling(fetcher, 15000);
}
