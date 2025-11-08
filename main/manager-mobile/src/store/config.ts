import type { PublicConfig } from '@/api/auth'
import { getPublicConfig } from '@/api/auth'
import { defineStore } from 'pinia'
import { ref } from 'vue'

// initialization_state
const initialConfigState: PublicConfig = {
  enableMobileRegister: false,
  version: '',
  year: '',
  allowUserRegister: false,
  mobileAreaList: [],
  beianIcpNum: '',
  beianGaNum: '',
  sm2PublicKey: '',
  name: import.meta.env.VITE_APP_TITLE,
}

export const useConfigStore = defineStore(
  'config',
  () => {
    // define_global_configuration
    const config = ref<PublicConfig>({ ...initialConfigState })

    // set_configuration_information
    const setConfig = (val: PublicConfig) => {
      config.value = val
    }

    // get_public_configuration
    const fetchPublicConfig = async () => {
      try {
        const configData = await getPublicConfig()
        console.log(configData)

        setConfig(configData)
        return configData
      }
      catch (error) {
        console.error('获取公共配置失败:', error)
        throw error
      }
    }

    // reset_configuration
    const resetConfig = () => {
      config.value = { ...initialConfigState }
    }

    return {
      config,
      setConfig,
      fetchPublicConfig,
      resetConfig,
    }
  },
  {
    persist: {
      key: 'config',
      serializer: {
        serialize: state => JSON.stringify(state.config),
        deserialize: value => ({ config: JSON.parse(value) }),
      },
    },
  },
)
