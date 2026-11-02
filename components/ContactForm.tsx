"use client";

import { useState } from "react";

// 種別は日本語と英語を併記する（医療機関からの連絡は日本語が中心。他言語の訳は突き合わせ前のため使わない）
const TYPES = [
  "掲載内容の訂正 / Correction",
  "掲載の取り下げ・非表示 / Remove a listing",
  "その他 / Other",
];

const field = "w-full rounded border border-line bg-white px-3 py-2.5 text-base focus:border-ink focus:outline-none";

export default function ContactForm() {
  const [status, setStatus] = useState<"idle" | "sending" | "done" | "error">("idle");

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    setStatus("sending");
    try {
      const res = await fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(new FormData(form).entries())),
      });
      if (!res.ok) throw new Error(String(res.status));
      setStatus("done");
      form.reset();
    } catch {
      setStatus("error");
    }
  }

  if (status === "done") {
    return (
      <div className="rounded border border-line bg-white p-6">
        <p className="font-bold">送信しました。/ Your message has been sent.</p>
        <p className="mt-2 text-sm text-ink/70">
          内容を確認のうえ、メールでご返信します。/ We will reply by email after reviewing your message.
        </p>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5">
      <div>
        <label htmlFor="type" className="mb-1.5 block text-sm font-bold">
          お問い合わせの種類 / Type *
        </label>
        <select id="type" name="type" required className={field}>
          {TYPES.map((t) => (
            <option key={t} value={t}>
              {t}
            </option>
          ))}
        </select>
      </div>
      <div>
        <label htmlFor="facility" className="mb-1.5 block text-sm font-bold">
          医療機関名・ページのURL / Facility name or page URL
        </label>
        <input id="facility" name="facility" type="text" maxLength={200} className={field} />
      </div>
      <div>
        <label htmlFor="name" className="mb-1.5 block text-sm font-bold">
          お名前 / Name *
        </label>
        <input id="name" name="name" type="text" required maxLength={60} className={field} />
      </div>
      <div>
        <label htmlFor="email" className="mb-1.5 block text-sm font-bold">
          メールアドレス / Email *
        </label>
        <input id="email" name="email" type="email" required maxLength={254} className={field} />
      </div>
      <div>
        <label htmlFor="message" className="mb-1.5 block text-sm font-bold">
          内容 / Message *
        </label>
        <textarea id="message" name="message" required minLength={10} maxLength={4000} rows={8} className={field} />
      </div>
      {/* honeypot：人には見えない欄。入力があれば bot として捨てる */}
      <div className="hidden" aria-hidden="true">
        <label htmlFor="website">Website</label>
        <input id="website" name="website" type="text" tabIndex={-1} autoComplete="off" />
      </div>
      {status === "error" && (
        <p className="text-sm font-bold text-accent">
          送信できませんでした。時間をおいてもう一度お試しください。/ Sending failed. Please try again later.
        </p>
      )}
      <button
        type="submit"
        disabled={status === "sending"}
        className="rounded bg-ink px-5 py-2.5 font-bold text-white disabled:opacity-60"
      >
        {status === "sending" ? "送信中… / Sending…" : "送信する / Send"}
      </button>
    </form>
  );
}
