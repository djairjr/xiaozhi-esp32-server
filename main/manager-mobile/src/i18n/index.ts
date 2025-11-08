import { ref } from 'vue'
import { useLangStore } from '@/store/lang'
import type { Language } from '@/store/lang'

// import_translation_files_for_each_language
import zhCN from './zh_CN'
import en from './en'
import zhTW from './zh_TW'

// language_pack_mapping
const messages = {
  zh_CN: zhCN,
  en,
  zh_TW: zhTW,
}

// current_language
const currentLang = ref<Language>('zh_CN')

// initialization_language
export function initI18n() {
  const langStore = useLangStore()
  currentLang.value = langStore.currentLang
}

// switch_language
export function changeLanguage(lang: Language) {
  currentLang.value = lang
  const langStore = useLangStore()
  langStore.changeLang(lang)
}

// get_translated_text
export function t(key: string, params?: Record<string, string | number>): string {
  const langMessages = messages[currentLang.value]

  // find_flat_key_names_directly
  if (langMessages && typeof langMessages === 'object' && key in langMessages) {
    let value = langMessages[key]
    if (typeof value === 'string') {
      // handle_parameter_substitution
      if (params) {
        let result = value
        Object.entries(params).forEach(([paramKey, paramValue]) => {
          const regex = new RegExp(`\{${paramKey}\}`, 'g')
          result = result.replace(regex, String(paramValue))
        })
        return result
      }
      return value
    }
    return key
  }

  return key // if_the_corresponding_translation_cannot_be_found，return_the_key_itself
}

// get_current_language
export function getCurrentLanguage(): Language {
  return currentLang.value
}

// get_a_list_of_supported_languages
export function getSupportedLanguages(): {code: Language, name: string}[] {
  return [
    { code: 'zh_CN', name: '简体中文' },
    { code: 'en', name: 'English' },
    { code: 'zh_TW', name: '繁體中文' },
  ]
}