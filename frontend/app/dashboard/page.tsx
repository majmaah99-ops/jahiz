"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Navbar from "@/components/Navbar";
import ScoreCard from "@/components/ScoreCard";
import ForecastChart from "@/components/ForecastChart";
import FactorsList from "@/components/FactorsList";
import LiquidityAlert from "@/components/LiquidityAlert";
import LoadingSpinner from "@/components/LoadingSpinner";
import { analyzeBusiness, getForecast } from "@/lib/api";
import type { AnalyzeResponse, ForecastPoint } from "@/lib/types";
import { Download, FileText, RefreshCw } from "lucide-react";

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<AnalyzeResponse | null>(null);
  const [forecast, setForecast] = useState<ForecastPoint[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const [analysis, fc] = await Promise.all([
          analyzeBusiness(),
          getForecast(),
        ]);
        setData(analysis);
        setForecast(fc);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <main className="min-h-screen">
      <Navbar />

      <div className="mx-auto max-w-7xl px-6 py-10">
        {loading || !data ? (
          <LoadingSpinner message="جاري تحليل المنشأة..." />
        ) : (
          <div className="animate-fade-in space-y-6">
            {/* Header */}
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-3xl font-bold text-white">
                  لوحة تحكم المنشأة
                </h1>
                <p className="text-slate-400 mt-1">
                  Cairo Café • الرياض • قطاع الأغذية والمشروبات
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => window.location.reload()}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg glass border border-dark-700 text-slate-300 hover:text-white transition"
                >
                  <RefreshCw className="w-4 h-4" />
                  تحديث
                </button>
                <button
                  onClick={() => router.push("/report")}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-brand-500 text-white hover:bg-brand-600 transition"
                >
                  <FileText className="w-4 h-4" />
                  تقرير البنك
                </button>
              </div>
            </div>

            {/* Liquidity Alert */}
            <LiquidityAlert forecast={data.liquidity_forecast} />

            {/* Main Grid */}
            <div className="grid lg:grid-cols-3 gap-6">
              <div className="lg:col-span-1">
                <ScoreCard
                  score={data.jahiz_ready_score}
                  tier={data.tier}
                  verdict={data.verdict}
                  suggestedAmount={data.suggested_amount}
                />
              </div>

              <div className="lg:col-span-2 space-y-6">
                <ForecastChart data={forecast} />
              </div>
            </div>

            {/* Factors */}
            <FactorsList factors={data.top_factors} />
          </div>
        )}
      </div>
    </main>
  );
}
