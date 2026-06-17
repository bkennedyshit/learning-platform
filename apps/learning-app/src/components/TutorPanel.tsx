"use client";

import React, { useState } from "react";
import styles from "./TutorPanel.module.css";

interface Message {
  id: string;
  role: "tutor" | "learner";
  text: string;
  citation?: string;
}

export interface TutorContext {
  title: string;
  text: string;
}

export default function TutorPanel({ context }: { context?: TutorContext }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "tutor",
      text: context?.title
        ? `Hi! Ask me anything about "${context.title}" and I'll answer from the lesson.`
        : "Hello! Ask me about the lesson material and I'll help.",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    const question = input.trim();
    if (!question || loading) return;

    const learnerMsg: Message = { id: Date.now().toString(), role: "learner", text: question };
    setMessages((prev) => [...prev, learnerMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch("/api/tutor", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          question,
          lessonTitle: context?.title,
          lessonText: context?.text,
        }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          role: "tutor",
          text: data.answer ?? "No response.",
          citation: data.grounded && context?.title ? `Grounded in: ${context.title}` : undefined,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: (Date.now() + 1).toString(), role: "tutor", text: "Something went wrong. Try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.panel}>
      <div className={styles.header}>
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M12 2a10 10 0 1 0 10 10H12V2z" />
          <path d="M12 12 2.1 7.1" />
          <path d="m12 12 7.1 7.1" />
        </svg>
        AI Tutor
      </div>

      <div className={styles.chatHistory}>
        {messages.map((m) => (
          <div key={m.id} className={`${styles.message} ${styles[m.role]}`}>
            <div>{m.text}</div>
            {m.citation && <span className={styles.citation}>{m.citation}</span>}
          </div>
        ))}
        {loading && (
          <div className={`${styles.message} ${styles.tutor}`}>
            <div>Thinking…</div>
          </div>
        )}
      </div>

      <div className={styles.inputArea}>
        <input
          className={styles.input}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask about this lesson..."
          disabled={loading}
        />
        <button className={styles.sendButton} onClick={handleSend} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
