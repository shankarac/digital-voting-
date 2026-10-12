import { useEffect, useState } from "react";
import { formatRemaining } from "../format";

export function Countdown({ deadline, status }) {
  const [, setTick] = useState(0);

  useEffect(() => {
    if (status !== "active") return undefined;
    const id = setInterval(() => setTick((value) => value + 1), 1000);
    return () => clearInterval(id);
  }, [status, deadline]);

  if (status === "closed") return <span>Closed by an admin</span>;
  if (status === "expired") return <span>Deadline passed</span>;
  return <time dateTime={deadline}>{formatRemaining(deadline)}</time>;
}
