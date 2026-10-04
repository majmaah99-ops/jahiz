"use client";

import { TrendingUp, TrendingDown } from "lucide-react";
import clsx from "clsx";
import { FEATURE_LABELS, type TopFactor } from "@/lib/types";

interface Props {
  factors: TopFactor[];
}

export default function FactorsList({ factors }: Props) {
  const maxImpact = Math.max(...factors.map((f) => Math.abs(f.impact)));

  return (
    <div className="glass rounded-2xl p-6 border border-dark-700">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-white">المحركات الرئيسية للسكور</h3>
        <p className="text-sm text-slate-400 mt-1">
          تفسير SHAP — يوضح لماذا هذا السكور بالضبط
        </p>
      </div>

      <div className="space-y-4">
        {factors.map((factor) => {
          const positive = factor.impact > 0;
          const width = (Math.abs(factor.impact) / maxImpact) * 100;
          const label = FEATURE_LABELS[factor.feature] || factor.feature;

          return (
            <div key={factor.feature} className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  {positive ? (
                    <TrendingUp className="w-4 h-4 text-brand-500" />
                  ) : (
                    <TrendingDown className="w-4 h-4 text-red-400" />
                  )}
                  <span className="text-slate-200 font-medium">{label}</span>
                </div>
                <span
                  className={clsx(
                    "font-mono text-xs px-2 py-0.5 rounded",
                    positive
                      ? "text-brand-500 bg-brand-500/10"
                      : "text-red-400 bg-red-500/10"
                  )}
                >
                  {factor.impact > 0 ? "+" : ""}
                  {factor.impact.toFixed(3)}
                </span>
              </div>
              <div className="h-2 rounded-full bg-dark-700 overflow-hidden">
                <div
                  className={clsx(
                    "h-full rounded-full transition-all duration-1000",
                    positive
                      ? "bg-gradient-to-l from-brand-500 to-teal-400"
                      : "bg-gradient-to-l from-red-500 to-orange-400"
                  )}
                  style={{ width: `${width}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
