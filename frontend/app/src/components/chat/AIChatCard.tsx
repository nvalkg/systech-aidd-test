"use client";

import { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import { Send, Trash2, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { apiClient } from "@/lib/api";
import { ChatMode } from "@/types/api";
import { Switch } from "@/components/ui/switch";
import { Collapsible, CollapsibleContent } from "@/components/ui/collapsible";

interface Message {
  sender: "ai" | "user";
  text: string;
  sql_query?: string;
}

interface AIChatCardProps {
  className?: string;
}

export default function AIChatCard({ className }: AIChatCardProps) {
  const [messages, setMessages] = useState<Message[]>([
    { sender: "ai", text: "👋 Hello! I'm your AI assistant." },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [mode, setMode] = useState<ChatMode>("normal");
  const [sessionId, setSessionId] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize session ID
  useEffect(() => {
    let id = localStorage.getItem("aidd-chat-session-id");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("aidd-chat-session-id", id);
    }
    setSessionId(id);
  }, []);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { sender: "user", text: userMessage }]);
    setIsTyping(true);
    setError(null);

    try {
      const response = await apiClient.sendChatMessage({
        session_id: sessionId,
        message: userMessage,
        mode: mode,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: response.response,
          sql_query: response.sql_query,
        },
      ]);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to send message"
      );
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "❌ Sorry, I encountered an error. Please try again.",
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleClear = async () => {
    if (!sessionId) return;

    try {
      await apiClient.clearChatHistory(sessionId);
      setMessages([
        {
          sender: "ai",
          text:
            mode === "admin"
              ? "📊 Admin mode cleared. Ask me about your conversation statistics!"
              : "👋 History cleared. How can I help you?",
        },
      ]);
      setError(null);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to clear history"
      );
    }
  };

  const handleModeChange = async (checked: boolean) => {
    const newMode: ChatMode = checked ? "admin" : "normal";
    setMode(newMode);

    // Add system message about mode change
    setMessages((prev) => [
      ...prev,
      {
        sender: "ai",
        text: checked
          ? "📊 Admin mode activated! Ask me questions about conversation statistics and analytics."
          : "💬 Normal mode activated! I'm your general AI assistant.",
      },
    ]);
  };

  return (
    <div
      className={cn(
        "relative w-[360px] h-[560px] rounded-2xl overflow-hidden p-[2px]",
        className
      )}
    >
      {/* Animated Outer Border */}
      <motion.div
        className="absolute inset-0 rounded-2xl border-2 border-white/20"
        animate={{ rotate: [0, 360] }}
        transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
      />

      {/* Inner Card */}
      <div className="relative flex flex-col w-full h-full rounded-xl border border-white/10 overflow-hidden bg-black/90 backdrop-blur-xl">
        {/* Inner Animated Background */}
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-gray-800 via-black to-gray-900"
          animate={{ backgroundPosition: ["0% 0%", "100% 100%", "0% 0%"] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          style={{ backgroundSize: "200% 200%" }}
        />

        {/* Floating Particles */}
        {Array.from({ length: 20 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 rounded-full bg-white/10"
            animate={{
              y: ["0%", "-140%"],
              x: [Math.random() * 200 - 100, Math.random() * 200 - 100],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: 5 + Math.random() * 3,
              repeat: Infinity,
              delay: i * 0.5,
              ease: "easeInOut",
            }}
            style={{ left: `${Math.random() * 100}%`, bottom: "-10%" }}
          />
        ))}

        {/* Header */}
        <div className="px-4 pt-6 pb-3 border-b border-white/10 relative z-10">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-white">
              🤖 AI Assistant
            </h2>
            <button
              onClick={handleClear}
              className="p-1 rounded hover:bg-white/10 transition-colors"
              title="Clear history"
            >
              <Trash2 className="w-4 h-4 text-white/70" />
            </button>
          </div>

          {/* Mode Toggle */}
          <div className="flex items-center gap-2.5 mt-3 h-5">
            <div className="flex items-center h-full">
              <Switch
                id="admin-mode"
                checked={mode === "admin"}
                onCheckedChange={handleModeChange}
                className="data-[state=checked]:bg-white/30 data-[state=unchecked]:bg-white/10"
              />
            </div>
            <label
              htmlFor="admin-mode"
              className="text-xs text-white/70 cursor-pointer select-none"
            >
              Admin Mode (Analytics)
            </label>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 px-4 py-3 overflow-y-auto space-y-3 text-sm flex flex-col relative z-10">
          {messages.map((msg, i) => (
            <div key={i}>
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4 }}
                className={cn(
                  "px-3 py-2 rounded-xl max-w-[80%] shadow-md backdrop-blur-md",
                  msg.sender === "ai"
                    ? "bg-white/10 text-white self-start"
                    : "bg-white/30 text-black font-semibold self-end"
                )}
              >
                {msg.text}
              </motion.div>

              {/* SQL Query Display (for admin mode) */}
              {msg.sql_query && (
                <Collapsible className="mt-1 ml-3">
                  <CollapsibleContent>
                    <div className="text-xs text-white/50 bg-black/30 p-2 rounded border border-white/10 font-mono overflow-x-auto">
                      <pre className="whitespace-pre-wrap">{msg.sql_query}</pre>
                    </div>
                  </CollapsibleContent>
                </Collapsible>
              )}
            </div>
          ))}

          {/* AI Typing Indicator */}
          {isTyping && (
            <motion.div
              className="flex items-center gap-1 px-3 py-2 rounded-xl max-w-[30%] bg-white/10 self-start"
              initial={{ opacity: 0 }}
              animate={{ opacity: [0, 1, 0.6, 1] }}
              transition={{ repeat: Infinity, duration: 1.2 }}
            >
              <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
              <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-200"></span>
              <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-400"></span>
            </motion.div>
          )}

          {/* Error Display */}
          {error && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-start gap-2 px-3 py-2 rounded-xl bg-red-500/20 border border-red-500/30 text-white/90 text-xs"
            >
              <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5" />
              <span>{error}</span>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="flex items-center gap-2 p-3 border-t border-white/10 relative z-10">
          <input
            className="flex-1 px-3 py-2 text-sm bg-black/50 rounded-lg border border-white/10 text-white focus:outline-none focus:ring-1 focus:ring-white/50"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button
            onClick={handleSend}
            className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={!input.trim() || isTyping}
          >
            <Send className="w-4 h-4 text-white" />
          </button>
        </div>
      </div>
    </div>
  );
}
