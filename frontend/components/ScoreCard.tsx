"use client";

import { TrendingUp, Award, AlertCircle } from "lucide-react";
import clsx from "clsx";

interface Props {
  score: number;
  tier: string;
  verdict: string;
  suggestedAmount: number;
}

export default function ScoreCard({ score, tier, verdict, suggestedAmount }: Props) {
  const percentage = score / 1000;
  const circumference = 2 * Math.PI * 90;
  const offset = circumference * (1 - percentage);

  const isPlatinum = score >= 750;
  const isGold = score >= 600 && score < 750;
  const isSilver = score >= 450 && score < 600;

  const color = isPlatinum
    ? "#10B981"
    : isGold
    ? "#F59E0B"
    : isSilver
    ? "#94A3B8"
    : "#EF4444";

  return (
    <div className="glass rounded-2xl p-8 border border-dark-700">
      <div className="flex flex-col items-center gap-6">
        {/* Circular Score */}
        <div className="relative w-64 h-64">
          <svg className="transform -rotate-90 w-64 h-64">
            <circle
              cx="128"
              cy="128"
              r="90"
              stroke="#1F2937"
              strokeWidth="14"
              fill="none"
            />
            <circle
              cx="128"
              cy="128"
              r="90"
              stroke={color}
              strokeWidth="14"
              fill="none"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              className="transition-all duration-1000 ease-out"
              style={{ filter: `drop-shadow(0 0 12px ${color}80)` }}
            />
          </svg>
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <div className="text-6xl font-bold text-white">{score}</div>
            <div className="text-sm text-slate-400 mt-1">/ 1000</div>
          </div>
        </div>

        {/* Tier Badge */}
        <div
          className={clsx(
            "flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium",
            isPlatinum && "bg-brand-500/10 text-brand-500 border border-brand-500/30",
            isGold && "bg-amber-500/10 text-amber-500 border border-amber-500/30",
            isSilver && "bg-slate-500/10 text-slate-300 border border-slate-500/30",
            !isPlatinum && !isGold && !isSilver && "bg-red-500/10 text-red-500 border border-red-500/30"
          )}
        >
          <Award className="w-4 h-4" />
          {tier}
        </div>

        {/* Verdict */}
        <div className="text-center">
          <div className="text-lg font-semibold text-white">{verdict}</div>
        </div>

        {/* Suggested Amount */}
        <div className="w-full mt-2 p-5 rounded-xl bg-dark-800 border border-dark-700">
          <div className="flex items-center justify-between">
            <div>
              <div className="text-sm text-slate-400">مبلغ التمويل المقترح</div>
              <div className="text-3xl font-bold text-brand-500 mt-1">
                {suggestedAmount.toLocaleString("ar-SA")} ر.س
              </div>
            </div>
            <div className="w-12 h-12 rounded-xl bg-brand-500/10 flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-brand-500" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
