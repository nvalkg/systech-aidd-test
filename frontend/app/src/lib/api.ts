import {
  ChatClearRequest,
  ChatMessage,
  ChatResponse,
  DashboardStats,
  Period,
} from "@/types/api";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string = API_BASE_URL) {
    this.baseUrl = baseUrl;
  }

  async getStats(period: Period): Promise<DashboardStats> {
    const response = await fetch(`${this.baseUrl}/api/stats?period=${period}`);
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return response.json();
  }

  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseUrl}/api/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }
    return response.json();
  }

  async sendChatMessage(request: ChatMessage): Promise<ChatResponse> {
    const response = await fetch(`${this.baseUrl}/api/chat/message`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Chat API error: ${response.status}`);
    }

    return response.json();
  }

  async clearChatHistory(sessionId: string): Promise<void> {
    const request: ChatClearRequest = { session_id: sessionId };

    const response = await fetch(`${this.baseUrl}/api/chat/clear`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Clear history error: ${response.status}`);
    }
  }
}

export const apiClient = new ApiClient();
