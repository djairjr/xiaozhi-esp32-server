/**
 * tabbar state，increase storageSync make_sure_to_refresh_the_browser_in_the_correct tabbar page
 * use_reactive_simple_state，instead_of pinia global_state
 */
export const tabbarStore = reactive({
  curIdx: uni.getStorageSync('app-tabbar-index') || 0,
  setCurIdx(idx: number) {
    this.curIdx = idx
    uni.setStorageSync('app-tabbar-index', idx)
  },
})
