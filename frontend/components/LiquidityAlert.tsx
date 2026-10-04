"use client";

import { AlertTriangle, CheckCircle2 } from "lucide-react";
import type { LiquidityForecast } from "@/lib/types";

interface Props {
  forecast: LiquidityForecast;
}

export default function LiquidityAlert({ forecast }: Props) {
  const hasGap = forecast.first_gap_date !== null;

  if (!hasGap) {
    return (
      <div className="rounded-2xl p-6 bg-brand-500/10 border border-brand-500/30 flex items-center gap-4">
        <div className="w-12 h-12 rounded-xl bg-brand-500/20 flex items-center justify-center shrink-0">
          <CheckCircle2 className="w-6 h-6 text-brand-500" />
        </div>
        <div>
          <div className="font-semibold text-white">لا توجد فجوات سيولة متوقعة</div>
          <div className="text-sm text-slate-300 mt-1">
            التدفق النقدي مستقر خلال الـ 45 يوماً القادمة
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="relative rounded-2xl p-6 bg-red-500/10 border border-red-500/30 overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/20 rounded-full blur-3xl" />
      <div className="relative flex items-start gap-4">
        <div className="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center shrink-0">
          <AlertTriangle className="w-6 h-6 text-red-500" />
        </div>
        <div className="flex-1">
          <div className="font-semibold text-white text-lg">
            ⚠️ فجوة سيولة متوقعة
          </div>
          <div className="text-slate-300 mt-2 leading-relaxed">
            بناءً على نمط فواتيرك الحالي، من المتوقع حدوث عجز بمقدار{" "}
            <span className="font-bold text-red-400">
              {forecast.max_gap_amount.toLocaleString("ar-SA")} ريال
            </span>{" "}
            بتاريخ{" "}
            <span className="font-bold text-white">{forecast.first_gap_date}</span>
          </div>
          <div className="mt-4 flex flex-wrap gap-3 text-xs">
            <div className="px-3 py-1.5 rounded-lg bg-dark-800 border border-dark-700">
              <span className="text-slate-400">التدفق المتوقع: </span>
              <span className="font-semibold text-brand-500">
                {forecast.forecast_total_inflow.toLocaleString("ar-SA")} ر.س
              </span>
            </div>
            <div className="px-3 py-1.5 rounded-lg bg-dark-800 border border-dark-700">
              <span className="text-slate-400">المصاريف المتوقعة: </span>
              <span className="font-semibold text-red-400">
                {forecast.forecast_total_outflow.toLocaleString("ar-SA")} ر.س
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
