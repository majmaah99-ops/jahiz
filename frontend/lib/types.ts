export interface AnalyzeResponse {
  jahiz_ready_score: number;
  tier: string;
  verdict: string;
  suggested_amount: number;
  top_factors: TopFactor[];
  liquidity_forecast: LiquidityForecast;
  bank_report: string;
  features: Record<string, number>;
}

export interface TopFactor {
  feature: string;
  value: number;
  impact: number;
}

export interface LiquidityForecast {
  first_gap_date: string | null;
  max_gap_amount: number;
  forecast_total_inflow: number;
  forecast_total_outflow: number;
}

export interface ForecastPoint {
  ds: string;
  yhat: number;
  yhat_lower: number;
  yhat_upper: number;
  cumulative: number;
}

export const FEATURE_LABELS: Record<string, string> = {
  customer_hhi: "تركيز العملاء",
  dso_days: "أيام التحصيل (DSO)",
  cashflow_volatility: "تذبذب التدفق النقدي",
  invoice_value_trend: "نمو قيمة الفاتورة",
  seasonality_strength: "قوة الموسمية",
  fixed_cost_ratio: "نسبة المصاريف الثابتة",
  supplier_delay_days: "تأخر سداد الموردين",
  monthly_revenue_avg: "متوسط الإيراد الشهري",
};
