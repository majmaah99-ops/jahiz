"use client";

export default function LoadingSpinner({ message = "جاري التحليل..." }: { message?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-6">
      <div className="relative">
        <div className="w-20 h-20 rounded-full border-4 border-dark-700" />
        <div className="absolute inset-0 w-20 h-20 rounded-full border-4 border-transparent border-t-brand-500 animate-spin" />
        <div className="absolute inset-4 w-12 h-12 rounded-full bg-brand-500/20 animate-pulse-slow" />
      </div>
      <div className="text-center">
        <div className="text-lg font-semibold text-white">{message}</div>
        <div className="text-sm text-slate-400 mt-2">
          نحلل 1,200 فاتورة + 45 يوماً من التنبؤات...
        </div>
      </div>
    </div>
  );
}
