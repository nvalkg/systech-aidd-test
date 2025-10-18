export type Period = "day" | "week" | "month";

export interface MetricCard {
  title: string;
  value: string;
  trend: number;
  trend_label: string;
  description: string;
}

export interface TimeSeriesPoint {
  timestamp: string;
  value: number;
}

export interface ConversationItem {
  conversation_id: number;
  user_id: number;
  messages_count: number;
  last_activity: string;
  created_at: string;
}

export interface TopUser {
  user_id: number;
  messages_count: number;
  conversations_count: number;
}

export interface DashboardStats {
  metrics: MetricCard[];
  activity_chart: TimeSeriesPoint[];
  recent_conversations: ConversationItem[];
  top_users: TopUser[];
  period: Period;
}

// Chat API types
export type ChatMode = "normal" | "admin";

export interface ChatMessage {
  session_id: string;
  message: string;
  mode: ChatMode;
}

export interface ChatResponse {
  response: string;
  mode: string;
  sql_query?: string;
}

export interface ChatClearRequest {
  session_id: string;
}
