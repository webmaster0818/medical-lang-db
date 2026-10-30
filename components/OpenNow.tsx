"use client";

import { useEffect, useState } from "react";
import type { Day } from "@/lib/data";

const DAYS: Day[] = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];

/** 日本時間の今の曜日・時刻で、届け出の診療時間内かを示す（祝日は判定しない） */
export function OpenNow({ hours, open, closed }: { hours: Partial<Record<Day, string[]>>[]; open: string; closed: string }) {
  const [state, setState] = useState<boolean | null>(null);
  useEffect(() => {
    const now = new Date(new Date().toLocaleString("en-US", { timeZone: "Asia/Tokyo" }));
    const day = DAYS[now.getDay()];
    const hm = now.getHours() * 60 + now.getMinutes();
    const toMin = (s: string) => {
      const [h, m] = s.split(":").map(Number);
      return h * 60 + (m || 0);
    };
    const isOpen = hours.some((h) =>
      (h[day] ?? []).some((range) => {
        const [a, b] = range.split("-");
        return a && b && toMin(a) <= hm && hm < toMin(b);
      }),
    );
    setState(isOpen);
  }, [hours]);
  if (state === null) return null;
  return (
    <span className={`text-xs font-bold ${state ? "text-tier-a" : "text-ink/50"}`}>{state ? `● ${open}` : closed}</span>
  );
}
