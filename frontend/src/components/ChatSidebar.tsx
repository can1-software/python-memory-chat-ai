import type { ChatListItem } from "../lib/api";

type ChatSidebarProps = {
  chats: ChatListItem[];
  selectedChatId: number | null;
  loading: boolean;
  onSelectChat: (chatId: number) => void;
  onCreateChat: () => void;
  creating: boolean;
};

export function ChatSidebar({
  chats,
  selectedChatId,
  loading,
  onSelectChat,
  onCreateChat,
  creating,
}: ChatSidebarProps) {
  return (
    <aside className="chat-sidebar">
      <div className="sidebar-header">
        <h2>Sohbetler</h2>
        <button type="button" onClick={onCreateChat} disabled={creating}>
          {creating ? "Oluşturuluyor..." : "Yeni Sohbet"}
        </button>
      </div>

      {loading ? (
        <p className="sidebar-info">Sohbetler yükleniyor...</p>
      ) : chats.length === 0 ? (
        <p className="sidebar-info">Henüz sohbet yok.</p>
      ) : (
        <ul className="chat-list">
          {chats.map((chat) => (
            <li key={chat.id}>
              <button
                type="button"
                className={`chat-list-item ${
                  selectedChatId === chat.id ? "active" : ""
                }`}
                onClick={() => onSelectChat(chat.id)}
              >
                {chat.title}
              </button>
            </li>
          ))}
        </ul>
      )}
    </aside>
  );
}
