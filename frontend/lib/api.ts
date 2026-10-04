import type { AnalyzeResponse, ForecastPoint } from "./types";
import { MOCK_ANALYZE, generateMockForecast } from "./mock";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
const USE_MOCK = process.env.NEXT_PUBLIC_USE_MOCK === "true";

export async function analyzeBusiness(): Promise<AnalyzeResponse> {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 1500));
    return MOCK_ANALYZE;
  }

  try {
    const res = await fetch(`${API_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn("Backend unavailable, falling back to mock data:", error);
    return MOCK_ANALYZE;
  }
}

export async function getForecast(): Promise<ForecastPoint[]> {
  if (USE_MOCK) {
    return generateMockForecast();
  }

  try {
    const res = await fetch(`${API_URL}/forecast`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return await res.json();
  } catch (error) {
    console.warn("Backend unavailable, using mock forecast");
    return generateMockForecast();
  }
}
