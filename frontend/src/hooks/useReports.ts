"use client";

import { useCallback } from "react";
import { api } from "@/lib/api";
import { usePolling } from "./usePolling";

export function useReports() {
  const fetcher = useCallback(() => api.getReports(), []);
  return usePolling(fetcher, 5000);
}
