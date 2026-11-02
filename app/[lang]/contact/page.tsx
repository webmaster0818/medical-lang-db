import type { Metadata } from "next";
import ContactForm from "@/components/ContactForm";
import { robots } from "@/lib/robots";

// 医療機関・利用者からの訂正・取り下げの受付。文言は日本語と英語の併記（他言語の訳は突き合わせ後に足す）
export const metadata: Metadata = {
  title: "お問い合わせ / Contact – MediLingo Japan",
  robots: robots(),
};

export default function Contact() {
  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="font-display text-3xl font-semibold">お問い合わせ / Contact</h1>
      <div className="space-y-2 text-sm leading-relaxed">
        <p>
          掲載内容の訂正、掲載の取り下げ・非表示のご依頼は、このフォームからご連絡ください。掲載は無料です。ご依頼の内容を確認のうえ、ご要望のとおりに対応します。
        </p>
        <p className="text-ink/70">
          Use this form to correct a listing or to ask us to remove one. Listing is free of charge. We will review your
          request and act on it as asked.
        </p>
        <p className="text-ink/70">
          このフォームでは診療のご相談・予約はお受けできません。急病のときは 119 に電話してください。/ We cannot answer
          medical questions or make appointments. In an emergency, call 119.
        </p>
      </div>
      <ContactForm />
    </div>
  );
}
