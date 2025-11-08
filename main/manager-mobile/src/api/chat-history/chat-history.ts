import type {
  ChatMessage,
  ChatSessionsResponse,
  GetSessionsParams,
} from './types'
import { http } from '@/http/request/alova'

/**
 * get_chat_session_list
 * @param agentId agent_id
 * @param params paging_parameters
 */
export function getChatSessions(agentId: string, params: GetSessionsParams) {
  return http.Get<ChatSessionsResponse>(`/agent/${agentId}/sessions`, {
    params,
    meta: {
      ignoreAuth: false,
      toast: false,
    },
    cacheFor: {
      expire: 0,
    },
  })
}

/**
 * get_chat_history_details
 * @param agentId agent_id
 * @param sessionId session_id
 */
export function getChatHistory(agentId: string, sessionId: string) {
  return http.Get<ChatMessage[]>(`/agent/${agentId}/chat-history/${sessionId}`, {
    meta: {
      ignoreAuth: false,
      toast: false,
    },
  })
}

/**
 * get_audio_download_id
 * @param audioId audio_id
 */
export function getAudioId(audioId: string) {
  return http.Post<string>(`/agent/audio/${audioId}`, {}, {
    meta: {
      ignoreAuth: false,
      toast: false,
    },
  })
}

/**
 * get_the_audio_playback_address
 * @param downloadId download_id
 */
export function getAudioPlayUrl(downloadId: string) {
  // according_to_the_requirements_document，this_returns_binary_directly，so_we_construct_the_url_directly
  return `/agent/play/${downloadId}`
}
