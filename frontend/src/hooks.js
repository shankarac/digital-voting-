import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "./api";
import { errorMessage, parseUtc } from "./format";

export function usePolled(url) {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const urlRef = useRef(url);
  const overdueRef = useRef("");
  urlRef.current = url;

  const refresh = useCallback(async (options = {}) => {
    const manual = options.manual === true;
    if (manual) {
      setRefreshing(true);
    }
    try {
      const response = await api.get(urlRef.current, {
        params: manual ? { _: Date.now() } : undefined,
        headers: manual ? { "Cache-Control": "no-cache", Pragma: "no-cache" } : undefined,
      });
      setData(response.data);
      setError("");
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
      if (manual) {
        setRefreshing(false);
      }
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    api
      .get(url)
      .then((response) => {
        if (!cancelled) {
          setData(response.data);
          setError("");
        }
      })
      .catch((err) => {
        if (!cancelled) setError(errorMessage(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    const interval = setInterval(() => {
      if (!document.hidden) refresh();
    }, 5000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [url, refresh]);

  useEffect(() => {
    const rows = (Array.isArray(data) ? data : data ? [data] : []).filter(
      (row) => row.status === "active" && row.deadline,
    );
    const overdueKey = rows
      .filter((row) => parseUtc(row.deadline).getTime() <= Date.now())
      .map((row) => row.id)
      .join(",");
    if (overdueKey && overdueRef.current !== overdueKey) {
      overdueRef.current = overdueKey;
      refresh();
      return undefined;
    }
    const wait = rows
      .map((row) => parseUtc(row.deadline).getTime() - Date.now())
      .filter((ms) => ms > 0)
      .sort((a, b) => a - b)[0];
    if (wait == null) return undefined;
    const timer = setTimeout(refresh, Math.min(wait + 300, 2147483647));
    return () => clearTimeout(timer);
  }, [data, refresh]);

  return { data, error, loading, refreshing, refresh };
}
