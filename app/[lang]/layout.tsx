import type { Metadata } from "next";
import Link from "next/link";
import "../globals.css";
import { LANGS, type SiteLang } from "@/lib/data";
import { BCP47, autonym, ui } from "@/lib/ui";
import { robots } from "@/lib/robots";

export const metadata: Metadata = {
  robots: robots(),
};

export function generateStaticParams() {
  return LANGS.map((lang) => ({ lang }));
}

export default async function LangLayout({ children, params }: { children: React.ReactNode; params: Promise<{ lang: string }> }) {
  const { lang } = await params;
  const t = ui(lang as SiteLang);
  return (
    <html lang={BCP47[lang as SiteLang]}>
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
          <nav aria-label="Language" className="mx-auto flex max-w-4xl flex-wrap gap-x-3 gap-y-1 px-4 pb-2 text-sm">
            {LANGS.map((l) => (
              <Link
                key={l}
                href={`/${l}/`}
                lang={BCP47[l]}
                aria-current={l === lang ? "page" : undefined}
                className={l === lang ? "font-bold no-underline" : "text-ink/70"}
              >
                {autonym(l)}
              </Link>
            ))}
          </nav>
        </header>
        <main className="mx-auto max-w-4xl px-4 py-6">{children}</main>
        <footer className="mt-12 border-t border-line">
          <div className="mx-auto max-w-4xl space-y-2 px-4 py-6 text-sm text-ink/70">
            <p>{t.disclaimer}</p>
            <p>
              {t.sources}: {t.srcMhlwNet} / {t.srcD5}
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
