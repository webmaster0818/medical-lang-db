import type { Metadata } from "next";
import Link from "next/link";
import "../globals.css";
import { LANGS, type SiteLang } from "@/lib/data";
import { UI } from "@/lib/ui";

// 公開前のプレビュー：全ページを検索に出さない（公開時に外す）
export const PREVIEW = true;

export const metadata: Metadata = {
  robots: PREVIEW ? { index: false, follow: false } : undefined,
};

export function generateStaticParams() {
  return LANGS.map((lang) => ({ lang }));
}

export default async function LangLayout({ children, params }: { children: React.ReactNode; params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  const t = UI[lang as "en"];
  return (
    <html lang={lang as SiteLang}>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="" />
        <link
          href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Fraunces:opsz,wght@9..144,600&family=Noto+Sans+JP:wght@400;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="min-h-screen">
        <header className="border-b border-line bg-paper">
          <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
            <Link href={`/${lang}/`} className="font-display text-xl font-semibold no-underline">
              {t.siteName}
            </Link>
            <a href="tel:119" className="rounded bg-accent px-3 py-1.5 text-sm font-bold text-white no-underline">
              119
            </a>
          </div>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-6">{children}</main>
        <footer className="mt-12 border-t border-line">
          <div className="mx-auto max-w-4xl space-y-2 px-4 py-6 text-sm text-ink/70">
            <p>{t.disclaimer}</p>
            <p>
              {t.sources}: Medical Information Net (Ministry of Health, Labour and Welfare) /{" "}
              List of medical institutions accepting foreign patients (Ministry of Health, Labour and Welfare)
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
