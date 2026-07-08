export type User = {
  id: number;
  name: string;
  email: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
};

export type ChatListItem = {
  id: number;
  title: string;
  created_at: string;
};

export type Chat = {
  id: number;
  title: string;
  user_id: number;
};

export type Message = {
  id: number;
  role: string;
  content: string;
  created_at: string;
};

export type ChatDetail = {
  id: number;
  title: string;
  messages: Message[];
};

export type MessageExchangeResponse = {
  user_message: Message;
  assistant_message: Message;
};

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

function getErrorMessage(data: unknown): string {
  if (!data || typeof data !== "object" || !("detail" in data)) {
    return "Bir hata oluştu.";
  }

  const detail = (data as { detail: unknown }).detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail) && detail.length > 0) {
    const first = detail[0];
    if (typeof first === "object" && first && "msg" in first) {
      return String(first.msg);
    }
  }

  return "Bir hata oluştu.";
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem("access_token");
  const headers = new Headers(options.headers);

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }

  let response: Response;

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers,
    });
  } catch {
    throw new ApiError(
      "Backend bağlantı hatası. Sunucunun çalıştığından emin olun.",
      0,
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new ApiError(getErrorMessage(data), response.status);
  }

  return data as T;
}

export const api = {
  register: (body: { name: string; email: string; password: string }) =>
    request<User>("/auth/register", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  login: (body: { email: string; password: string }) =>
    request<LoginResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    }),

  me: () => request<User>("/auth/me"),

  getChats: () => request<ChatListItem[]>("/chats"),

  createChat: (title: string) =>
    request<Chat>("/chats", {
      method: "POST",
      body: JSON.stringify({ title }),
    }),

  getChat: (chatId: number) => request<ChatDetail>(`/chats/${chatId}`),

  sendMessage: (chatId: number, content: string) =>
    request<MessageExchangeResponse>(`/chats/${chatId}/messages`, {
      method: "POST",
      body: JSON.stringify({ content }),
    }),
};
