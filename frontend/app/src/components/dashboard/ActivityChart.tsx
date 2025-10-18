"use client";

import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { TimeSeriesPoint, Period } from "@/types/api";
import { format } from "date-fns";

interface ActivityChartProps {
  data: TimeSeriesPoint[];
  period: Period;
}

export function ActivityChart({ data, period }: ActivityChartProps) {
  // Format the data for recharts
  const chartData = data.map((point) => ({
    timestamp: point.timestamp,
    value: point.value,
    displayTime: formatTimestamp(point.timestamp, period),
  }));

  return (
    <Card>
      <CardHeader>
        <CardTitle>Activity Chart</CardTitle>
        <p className="text-sm text-muted-foreground">
          Message activity for the selected period
        </p>
      </CardHeader>
      <CardContent>
        <ResponsiveContainer width="100%" height={350}>
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" className="stroke-muted" />
            <XAxis
              dataKey="displayTime"
              className="text-xs"
              tick={{ fill: "#ffffff" }}
            />
            <YAxis className="text-xs" tick={{ fill: "#ffffff" }} />
            <Tooltip
              contentStyle={{
                backgroundColor: "hsl(var(--background))",
                border: "1px solid hsl(var(--border))",
                borderRadius: "var(--radius)",
              }}
              labelStyle={{ color: "hsl(var(--foreground))" }}
            />
            <Area
              type="monotone"
              dataKey="value"
              stroke="#8884d8"
              fillOpacity={1}
              fill="url(#colorValue)"
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}

function formatTimestamp(timestamp: string, period: Period): string {
  const date = new Date(timestamp);

  switch (period) {
    case "day":
      return format(date, "HH:mm");
    case "week":
      return format(date, "EEE");
    case "month":
      return format(date, "MMM d");
    default:
      return format(date, "MMM d");
  }
}
