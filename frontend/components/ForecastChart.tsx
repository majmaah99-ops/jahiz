"use client";

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
} from "recharts";
import type { ForecastPoint } from "@/lib/types";

interface Props {
  data: ForecastPoint[];
}

export default function ForecastChart({ data }: Props) {
  const formatted = data.map((p) => ({
    ...p,
    date: new Date(p.ds).toLocaleDateString("ar-SA", {
      month: "short",
      day: "numeric",
    }),
  }));

  return (
    <div className="glass rounded-2xl p-6 border border-dark-700">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-white">تنبؤ السيولة (45 يوماً)</h3>
          <p className="text-sm text-slate-400 mt-1">
            Prophet + موسمية سعودية (رواتب، إيجار، رمضان)
          </p>
        </div>
        <div className="flex items-center gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-brand-500" />
            <span className="text-slate-300">التدفق اليومي</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-teal-400" />
            <span className="text-slate-300">الرصيد التراكمي</span>
          </div>
        </div>
      </div>

      <div className="h-72" dir="ltr">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={formatted}>
            <defs>
              <linearGradient id="colorYhat" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#10B981" stopOpacity={0.4} />
                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
              </linearGradient>
              <linearGradient id="colorCumulative" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#14B8A6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#14B8A6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1F2937" />
            <XAxis
              dataKey="date"
              stroke="#64748B"
              fontSize={11}
              tickMargin={10}
              interval={Math.floor(formatted.length / 8)}
            />
            <YAxis stroke="#64748B" fontSize={11} tickFormatter={(v) => `${(v / 1000).toFixed(0)}k`} />
            <Tooltip
              contentStyle={{
                backgroundColor: "#111827",
                border: "1px solid #1F2937",
                borderRadius: "12px",
                fontSize: "12px",
                direction: "rtl",
              }}
              labelStyle={{ color: "#94A3B8" }}
            />
            <ReferenceLine y={0} stroke="#EF4444" strokeDasharray="3 3" opacity={0.5} />
            <Area
              type="monotone"
              dataKey="yhat"
              stroke="#10B981"
              strokeWidth={2}
              fill="url(#colorYhat)"
              name="التدفق اليومي"
            />
            <Area
              type="monotone"
              dataKey="cumulative"
              stroke="#14B8A6"
              strokeWidth={2}
              strokeDasharray="5 5"
              fill="url(#colorCumulative)"
              name="الرصيد التراكمي"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
