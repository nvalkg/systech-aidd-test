"use client";

import { useEffect, useState } from "react";
import { DashboardHeader } from "@/components/dashboard/DashboardHeader";
import { PeriodSelector } from "@/components/dashboard/PeriodSelector";
import { MetricCards } from "@/components/dashboard/MetricCards";
import { ActivityChart } from "@/components/dashboard/ActivityChart";
import { ConversationsTable } from "@/components/dashboard/ConversationsTable";
import { TopUsersCard } from "@/components/dashboard/TopUsersCard";
import { MatrixBackground } from "@/components/dashboard/MatrixBackground";
import { FloatingChatButton } from "@/components/chat/FloatingChatButton";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";
import { apiClient } from "@/lib/api";
import type { DashboardStats, Period } from "@/types/api";

export default function DashboardPage() {
  const [period, setPeriod] = useState<Period>("week");
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStats() {
      try {
        setLoading(true);
        setError(null);
        const data = await apiClient.getStats(period);
        setStats(data);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to fetch statistics"
        );
      } finally {
        setLoading(false);
      }
    }

    fetchStats();
  }, [period]);

  return (
    <div className="flex min-h-screen flex-col relative">
      {/* Matrix animated background */}
      <MatrixBackground />

      {/* Content */}
      <div className="flex-1 space-y-6 p-8 relative z-10">
        <DashboardHeader />

        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <div className="flex items-center justify-between">
          <PeriodSelector value={period} onChange={setPeriod} />
        </div>

        {loading ? (
          <div className="space-y-6">
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              {[...Array(4)].map((_, i) => (
                <Skeleton key={i} className="h-32" />
              ))}
            </div>
            <Skeleton className="h-96" />
            <div className="grid gap-6 md:grid-cols-2">
              <Skeleton className="h-96" />
              <Skeleton className="h-96" />
            </div>
          </div>
        ) : stats ? (
          <>
            <MetricCards metrics={stats.metrics} />

            <ActivityChart data={stats.activity_chart} period={period} />

            <div className="grid gap-6 md:grid-cols-2">
              <ConversationsTable conversations={stats.recent_conversations} />
              <TopUsersCard users={stats.top_users} />
            </div>
          </>
        ) : null}
      </div>

      {/* Floating Chat Button */}
      <FloatingChatButton />
    </div>
  );
}
