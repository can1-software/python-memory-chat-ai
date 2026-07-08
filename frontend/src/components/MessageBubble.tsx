import type { Message } from "../lib/api";

type MessageBubbleProps = {
  message: Message;
};

export function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "user" : "assistant"}`}>
      <div className={`message-bubble ${isUser ? "user" : "assistant"}`}>
        <span className="message-role">{isUser ? "Sen" : "AI"}</span>
        <p>{message.content}</p>
      </div>
    </div>
  );
}
