"use client";

import { useCallback } from "react";
import { usePolling } from "./usePolling";
import { api } from "@/lib/api";

export function useAlerts(limit = 50) {
  const fetcher = useCallback(() => api.getAlerts(limit), [limit]);
  return usePolling(fetcher, 10000);
}
