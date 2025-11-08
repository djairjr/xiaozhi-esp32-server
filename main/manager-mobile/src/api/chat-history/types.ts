// chat_session_list_items
export interface ChatSession {
  sessionId: string
  createdAt: string
  chatCount: number
}

// chat_session_list_response
export interface ChatSessionsResponse {
  total: number
  list: ChatSession[]
}

// chat_messages
export interface ChatMessage {
  createdAt: string
  chatType: 1 | 2 // 1 is the user, 2 is the AI
  content: string
  audioId: string | null
  macAddress: string
}

// user_message_content（need_to_parse_json）
export interface UserMessageContent {
  speaker: string
  content: string
}

// get_chat_session_list_parameters
export interface GetSessionsParams {
  page: number
  limit: number
}

// audio_playback_related
export interface AudioResponse {
  data: string // audio_download_id
}
