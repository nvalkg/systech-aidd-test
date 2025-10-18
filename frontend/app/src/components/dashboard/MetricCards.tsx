import { MetricCard } from "./MetricCard";
import type { MetricCard as MetricCardType } from "@/types/api";

interface MetricCardsProps {
  metrics: MetricCardType[];
}

export function MetricCards({ metrics }: MetricCardsProps) {
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      {metrics.map((metric, index) => (
        <MetricCard key={index} metric={metric} />
      ))}
    </div>
  );
}
