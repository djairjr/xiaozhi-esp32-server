import { ref } from 'vue'
import { ref } from 'vue'
import { defineStore } from 'pinia'

// supported_language_types
export type Language = 'zh_CN' | 'en' | 'zh_TW'

export interface LangStore {
  currentLang: Language
  changeLang: (lang: Language) => void
}

export const useLangStore = defineStore(
  'lang',
  (): LangStore => {
    // get_language_settings_from_local_storage，if_not_use_default_value
    const savedLang = uni.getStorageSync('app_language') as Language | null
    const currentLang = ref<Language>(savedLang || 'zh_CN')

    // switch_language
    const changeLang = (lang: Language) => {
      currentLang.value = lang
      // save_language_settings_to_local_storage
      uni.setStorageSync('app_language', lang)
    }

    return {
      currentLang,
      changeLang,
    }
  },
  {
    persist: {
      key: 'lang',
      serializer: {
        serialize: state => JSON.stringify(state.currentLang),
        deserialize: value => ({ currentLang: JSON.parse(value) }),
      },
    },
  },
)