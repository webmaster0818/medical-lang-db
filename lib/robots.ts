import type { Metadata } from "next";

// 公開前のプレビュー：全ページを検索に出さない（公開時に false にし、public/robots.txt も外す）
export const PREVIEW = true;

/**
 * ページの robots。ページ側で robots を返すと layout の指定を上書きするので、
 * プレビュー中の noindex は必ずここを通して付ける
 */
export function robots(noindex = false): Metadata["robots"] {
  if (PREVIEW) return { index: false, follow: false };
  return noindex ? { index: false, follow: true } : undefined;
}
