import type {
  ChatHistory,
  CreateSpeakerData,
  VoicePrint,
} from './types'
import { http } from '@/http/request/alova'

// get_voiceprint_list
export function getVoicePrintList(agentId: string) {
  return http.Get<VoicePrint[]>(`/agent/voice-print/list/${agentId}`, {
    meta: {
      ignoreAuth: false,
      toast: false,
    },
    cacheFor: {
      expire: 0,
    },
  })
}

// get_voice_conversation_records（used_to_select_voiceprint_vectors）
export function getChatHistory(agentId: string) {
  return http.Get<ChatHistory[]>(`/agent/${agentId}/chat-history/user`, {
    meta: {
      ignoreAuth: false,
      toast: false,
    },
    cacheFor: {
      expire: 0,
    },
  })
}

// add_new_speaker
export function createVoicePrint(data: CreateSpeakerData) {
  return http.Post<null>('/agent/voice-print', data, {
    meta: {
      ignoreAuth: false,
      toast: true,
    },
  })
}

// delete_voiceprint
export function deleteVoicePrint(id: string) {
  return http.Delete<null>(`/agent/voice-print/${id}`, {
    meta: {
      ignoreAuth: false,
      toast: true,
    },
  })
}

// update_voiceprint_information
export function updateVoicePrint(data: VoicePrint) {
  return http.Put<null>('/agent/voice-print', data, {
    meta: {
      ignoreAuth: false,
      toast: true,
    },
  })
}
