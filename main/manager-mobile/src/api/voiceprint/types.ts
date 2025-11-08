// voiceprint_information_response_type
export interface VoicePrint {
  id: string
  audioId: string
  sourceName: string
  introduce: string
  createDate: string
}

// voice_conversation_record_type
export interface ChatHistory {
  content: string
  audioId: string
}

// create_speaker_data_type
export interface CreateSpeakerData {
  agentId: string
  audioId: string
  sourceName: string
  introduce: string
}

// generic_response_types
export interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T
}
