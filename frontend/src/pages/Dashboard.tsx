import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, ApiError, type ChatListItem, type Message } from "../lib/api";
import { useAuth } from "../context/AuthContext";
import { ChatSidebar } from "../components/ChatSidebar";
import { ChatWindow } from "../components/ChatWindow";

export default function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [chats, setChats] = useState<ChatListItem[]>([]);
  const [selectedChatId, setSelectedChatId] = useState<number | null>(null);
  const [selectedChatTitle, setSelectedChatTitle] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);

  const [loadingChats, setLoadingChats] = useState(true);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [creatingChat, setCreatingChat] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");

  const handleAuthError = useCallback(
    (err: unknown) => {
      if (err instanceof ApiError && err.status === 401) {
        logout();
        navigate("/login");
        return true;
      }
      return false;
    },
    [logout, navigate],
  );

  const loadChats = useCallback(async () => {
    setLoadingChats(true);
    try {
      const data = await api.getChats();
      setChats(data);
    } catch (err) {
      if (!handleAuthError(err)) {
        setError(
          err instanceof ApiError
            ? err.message
            : "Sohbetler yüklenemedi.",
        );
      }
    } finally {
      setLoadingChats(false);
    }
  }, [handleAuthError]);

  const loadChat = useCallback(
    async (chatId: number) => {
      setLoadingMessages(true);
      setError("");
      try {
        const data = await api.getChat(chatId);
        setSelectedChatId(chatId);
        setSelectedChatTitle(data.title);
        setMessages(data.messages);
      } catch (err) {
        if (!handleAuthError(err)) {
          setError(
            err instanceof ApiError
              ? err.message
              : "Mesajlar yüklenemedi.",
          );
        }
      } finally {
        setLoadingMessages(false);
      }
    },
    [handleAuthError],
  );

  useEffect(() => {
    loadChats();
  }, [loadChats]);

  const handleCreateChat = async () => {
    setCreatingChat(true);
    setError("");
    try {
      const newChat = await api.createChat("Yeni Sohbet");
      await loadChats();
      await loadChat(newChat.id);
    } catch (err) {
      if (!handleAuthError(err)) {
        setError(
          err instanceof ApiError
            ? err.message
            : "Yeni sohbet oluşturulamadı.",
        );
      }
    } finally {
      setCreatingChat(false);
    }
  };

  const handleSendMessage = async (content: string) => {
    if (!selectedChatId) return;

    setSending(true);
    setError("");

    try {
      const response = await api.sendMessage(selectedChatId, content);
      setMessages((prev) => [
        ...prev,
        response.user_message,
        response.assistant_message,
      ]);
    } catch (err) {
      if (handleAuthError(err)) return;

      if (err instanceof ApiError && err.status === 500) {
        setError("AI cevabı alınamadı ama mesaj kaydedilmiş olabilir.");
        await loadChat(selectedChatId);
      } else {
        setError(
          err instanceof ApiError
            ? err.message
            : "Mesaj gönderilemedi.",
        );
      }
    } finally {
      setSending(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  if (!user) {
    return null;
  }

  return (
    <div className="chat-page">
      <header className="chat-topbar">
        <div>
          <h1>Memory Chat AI</h1>
          <p className="user-info">
            {user.name} · {user.email}
          </p>
        </div>
        <button type="button" onClick={handleLogout} className="secondary-button">
          Logout
        </button>
      </header>

      <div className="chat-layout">
        <ChatSidebar
          chats={chats}
          selectedChatId={selectedChatId}
          loading={loadingChats}
          onSelectChat={loadChat}
          onCreateChat={handleCreateChat}
          creating={creatingChat}
        />

        <ChatWindow
          chatTitle={selectedChatTitle}
          messages={messages}
          loading={loadingMessages}
          sending={sending}
          error={error}
          onSendMessage={handleSendMessage}
        />
      </div>
    </div>
  );
}
