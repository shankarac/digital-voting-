export function normalizeName(value) {
  return value.trim().replace(/\s+/g, " ");
}

export function parseUtc(value) {
  if (!value) return new Date(NaN);
  const hasZone = /[zZ]|[+-]\d{2}:\d{2}$/.test(value);
  return new Date(hasZone ? value : `${value}Z`);
}

export function formatWhen(value) {
  const date = parseUtc(value);
  if (Number.isNaN(date.getTime())) return "";
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function formatRemaining(deadline) {
  const ms = parseUtc(deadline).getTime() - Date.now();
  if (ms <= 0) return "Deadline reached";
  const total = Math.floor(ms / 1000);
  const days = Math.floor(total / 86400);
  const hours = Math.floor((total % 86400) / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const seconds = total % 60;
  if (days > 0) return `${days}d ${hours}h ${minutes}m`;
  if (hours > 0) return `${hours}h ${minutes}m ${seconds}s`;
  return `${minutes}m ${seconds}s`;
}

export function errorMessage(error) {
  const detail = error?.response?.data?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || "Invalid value").join(" ");
  }
  if (!error?.response) {
    return "Cannot reach the voting API. Start the backend on port 8000.";
  }
  return "Request failed";
}

export function percent(count, total) {
  if (!total) return 0;
  return Math.round((count / total) * 1000) / 10;
}
