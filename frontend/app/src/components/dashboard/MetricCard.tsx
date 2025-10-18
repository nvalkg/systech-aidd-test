import { TrendingUp, TrendingDown } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { MetricCard as MetricCardType } from "@/types/api";

interface MetricCardProps {
  metric: MetricCardType;
}

export function MetricCard({ metric }: MetricCardProps) {
  const isPositive = metric.trend >= 0;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{metric.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{metric.value}</div>
        <div className="flex items-center pt-1">
          <span
            className={`inline-flex items-center text-xs ${
              isPositive ? "text-green-600" : "text-red-600"
            }`}
          >
            {isPositive ? (
              <TrendingUp className="mr-1 h-3 w-3" />
            ) : (
              <TrendingDown className="mr-1 h-3 w-3" />
            )}
            {Math.abs(metric.trend).toFixed(1)}%
          </span>
          <span className="ml-2 text-xs text-muted-foreground">
            {metric.trend_label}
          </span>
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          {metric.description}
        </p>
      </CardContent>
    </Card>
  );
}
