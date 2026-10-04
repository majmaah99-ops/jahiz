"use client";

import { Check, Loader2, FileText, CreditCard, Landmark } from "lucide-react";
import clsx from "clsx";

type Status = "idle" | "connecting" | "connected";

interface Props {
  title: string;
  subtitle: string;
  icon: "zatca" | "mada" | "bank";
  status: Status;
  onClick: () => void;
}

const ICONS = {
  zatca: FileText,
  mada: CreditCard,
  bank: Landmark,
};

export default function ConnectCard({ title, subtitle, icon, status, onClick }: Props) {
  const Icon = ICONS[icon];

  return (
    <button
      onClick={onClick}
      disabled={status === "connected"}
      className={clsx(
        "group relative w-full text-right p-6 rounded-2xl border transition-all duration-300",
        status === "idle" && "glass border-dark-700 hover:border-brand-500/50 hover:glow",
        status === "connecting" && "glass border-brand-500/70 animate-pulse-slow",
        status === "connected" && "bg-brand-500/10 border-brand-500/50 cursor-default"
      )}
    >
      <div className="flex items-start gap-4">
        <div
          className={clsx(
            "w-12 h-12 rounded-xl flex items-center justify-center shrink-0 transition",
            status === "connected"
              ? "bg-brand-500 text-white"
              : "bg-dark-700 text-slate-300 group-hover:bg-brand-500/20 group-hover:text-brand-500"
          )}
        >
          <Icon className="w-6 h-6" />
        </div>

        <div className="flex-1">
          <div className="flex items-center justify-between">
            <div className="text-lg font-semibold text-white">{title}</div>
            <div className="shrink-0">
              {status === "idle" && (
                <span className="text-xs text-slate-400 border border-dark-700 rounded-full px-3 py-1">
                  غير مرتبط
                </span>
              )}
              {status === "connecting" && (
                <Loader2 className="w-5 h-5 text-brand-500 animate-spin" />
              )}
              {status === "connected" && (
                <span className="flex items-center gap-1 text-xs text-brand-500 bg-brand-500/10 rounded-full px-3 py-1">
                  <Check className="w-3 h-3" />
                  مرتبط
                </span>
              )}
            </div>
          </div>
          <div className="text-sm text-slate-400 mt-1">{subtitle}</div>
        </div>
      </div>
    </button>
  );
}
