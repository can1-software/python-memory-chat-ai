import { type FormEvent, useEffect, useRef, useState } from "react";
import type { Message } from "../lib/api";
import { MessageBubble } from "./MessageBubble";

type ChatWindowProps = {
  chatTitle: string | null;
  messages: Message[];
  loading: boolean;
  sending: boolean;
  error: string;
  onSendMessage: (content: string) => Promise<void>;
};

export function ChatWindow({
  chatTitle,
  messages,
  loading,
  sending,
  error,
  onSendMessage,
}: ChatWindowProps) {
  const [input, setInput] = useState("");
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const content = input.trim();
    if (!content || sending) return;

    setInput("");
    await onSendMessage(content);
  };

  if (!chatTitle) {
    return (
      <section className="chat-window empty">
        <p>Yeni bir sohbet başlat</p>
      </section>
    );
  }

  return (
    <section className="chat-window">
      <div className="chat-window-header">
        <h2>{chatTitle}</h2>
      </div>

      <div className="messages-area">
        {loading ? (
          <p className="window-info">Mesajlar yükleniyor...</p>
        ) : messages.length === 0 ? (
          <p className="window-info">Henüz mesaj yok. İlk mesajını yaz.</p>
        ) : (
          messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {error && <p className="error chat-error">{error}</p>}

      <form className="message-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Mesajını yaz..."
          disabled={sending}
        />
        <button type="submit" disabled={sending || !input.trim()}>
          {sending ? "Gönderiliyor..." : "Gönder"}
        </button>
      </form>
    </section>
  );
}
