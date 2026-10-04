"use client";

import { useEffect, useState } from "react";
import Navbar from "@/components/Navbar";
import LoadingSpinner from "@/components/LoadingSpinner";
import { analyzeBusiness } from "@/lib/api";
import type { AnalyzeResponse } from "@/lib/types";
import { Download, Printer, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function ReportPage() {
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const analysis = await analyzeBusiness();
      setData(analysis);
      setLoading(false);
    }
    load();
  }, []);

  const handleDownload = () => {
    if (!data) return;
    const blob = new Blob([data.bank_report], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `JAHIZ-Report-${new Date().toISOString().split("T")[0]}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <main className="min-h-screen">
      <Navbar />

      <div className="mx-auto max-w-5xl px-6 py-10">
        {loading || !data ? (
          <LoadingSpinner message="جاري توليد تقرير البنك..." />
        ) : (
          <div className="animate-fade-in">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <div>
                <Link
                  href="/dashboard"
                  className="inline-flex items-center gap-2 text-sm text-slate-400 hover:text-white mb-3 transition"
                >
                  <ArrowRight className="w-4 h-4" />
                  رجوع للوحة التحكم
                </Link>
                <h1 className="text-3xl font-bold text-white">تقرير البنك الذكي</h1>
                <p className="text-slate-400 mt-1">
                  جاهز للإرسال إلى البنك السعودي للاستثمار
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => window.print()}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg glass border border-dark-700 text-slate-300 hover:text-white transition"
                >
                  <Printer className="w-4 h-4" />
                  طباعة
                </button>
                <button
                  onClick={handleDownload}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-500 text-white hover:bg-brand-600 transition"
                >
                  <Download className="w-4 h-4" />
                  تحميل
                </button>
              </div>
            </div>

            {/* Report Body */}
            <div className="glass rounded-2xl border border-dark-700 overflow-hidden">
              <div className="px-6 py-4 border-b border-dark-700 bg-dark-800 flex items-center gap-3">
                <div className="w-3 h-3 rounded-full bg-red-500" />
                <div className="w-3 h-3 rounded-full bg-yellow-500" />
                <div className="w-3 h-3 rounded-full bg-green-500" />
                <span className="text-xs text-slate-400 mr-auto">
                  JAHIZ-Report-{new Date().toISOString().split("T")[0]}.txt
                </span>
              </div>
              <pre className="p-8 text-sm text-slate-200 font-mono whitespace-pre-wrap leading-relaxed overflow-x-auto">
                {data.bank_report}
              </pre>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
