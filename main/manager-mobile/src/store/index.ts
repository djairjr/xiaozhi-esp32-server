import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate' // data_persistence

const store = createPinia()
store.use(
  createPersistedState({
    storage: {
      getItem: uni.getStorageSync,
      setItem: uni.setStorageSync,
    },
  }),
)

export default store

export * from './config'
export * from './plugin'
// unified_export_of_modules
export * from './user'
