"use client";

import { useState } from "react";
import { api } from "@/lib/api";

export function useWatch() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastReportId, setLastReportId] = useState<string | null>(null);

  const trigger = async (topic: string) => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.triggerWatch(topic);
      setLastReportId(result.report_id);
      return result.report_id;
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to trigger watch");
      return null;
    } finally {
      setLoading(false);
    }
  };

  return { trigger, loading, error, lastReportId };
}
