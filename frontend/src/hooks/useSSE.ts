"use client";

import { useEffect, useRef, useState, useCallback } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const MAX_BUFFER = 200;

interface SSEEvent {
  type: string;
  data: unknown;
  timestamp: number;
}

export function useSSE(path: string = "/news/stream") {
  const [events, setEvents] = useState<SSEEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const connect = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
    }

    const es = new EventSource(`${API_URL}${path}`);
    eventSourceRef.current = es;

    es.onopen = () => setConnected(true);

    es.addEventListener("news_analyzed", (e) => {
      try {
        const data = JSON.parse(e.data);
        setEvents((prev) => {
          const next = [{ type: "news_analyzed", data, timestamp: Date.now() }, ...prev];
          return next.slice(0, MAX_BUFFER);
        });
      } catch {
        // ignore parse errors
      }
    });

    es.addEventListener("alert_sent", (e) => {
      try {
        const data = JSON.parse(e.data);
        setEvents((prev) => {
          const next = [{ type: "alert_sent", data, timestamp: Date.now() }, ...prev];
          return next.slice(0, MAX_BUFFER);
        });
      } catch {
        // ignore parse errors
      }
    });

    es.onerror = () => {
      setConnected(false);
      es.close();
      // Reconnect after 5 seconds
      reconnectTimeoutRef.current = setTimeout(connect, 5000);
    };
  }, [path]);

  useEffect(() => {
    connect();
    return () => {
      eventSourceRef.current?.close();
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connect]);

  return { events, connected };
}
