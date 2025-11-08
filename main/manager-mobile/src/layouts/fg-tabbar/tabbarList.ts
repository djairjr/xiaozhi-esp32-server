import type { TabBar } from '@uni-helper/vite-plugin-uni-pages'

type FgTabBarItem = TabBar['list'][0] & {
  icon: string
  iconType: 'uiLib' | 'unocss' | 'iconfont'
}

/**
 * tabbar chosen_strategy，for_a_more_detailed_introduction_see tabbar.md document
 * 0: 'NO_TABBAR' `none tabbar`
 * 1: 'NATIVE_TABBAR'  `completely_native tabbar`
 * 2: 'CUSTOM_TABBAR_WITH_CACHE' `have_cache_customization tabbar`
 * 3: 'CUSTOM_TABBAR_WITHOUT_CACHE' `no_cache_customization tabbar`
 *
 * kind_tips：after_any_code_changes_in_this_file，all_need_to_be_rerun，otherwise pages.json will_not_update_causing_error
 */
export const TABBAR_MAP = {
  NO_TABBAR: 0,
  NATIVE_TABBAR: 1,
  CUSTOM_TABBAR_WITH_CACHE: 2,
  CUSTOM_TABBAR_WITHOUT_CACHE: 3,
}
// TODO：switch_the_strategy_of_using_tabbar_here
export const selectedTabbarStrategy = TABBAR_MAP.NATIVE_TABBAR

// selectedTabbarStrategy==NATIVE_TABBAR(1) hour，need_to_fill_in iconPath and selectedIconPath
// selectedTabbarStrategy==CUSTOM_TABBAR(2,3) hour，need_to_fill_in icon and iconType
// selectedTabbarStrategy==NO_TABBAR(0) hour，tabbarList not_effective
export const tabbarList: FgTabBarItem[] = [
  {
    iconPath: 'static/tabbar/robot.png',
    selectedIconPath: 'static/tabbar/robot_activate.png',
    pagePath: 'pages/index/index',
    text: '首页',
    icon: 'home',
    // select UI the_framework_comes_with icon hour，iconType for uiLib
    iconType: 'uiLib',
  },
  {
    iconPath: 'static/tabbar/network.png',
    selectedIconPath: 'static/tabbar/network_activate.png',
    pagePath: 'pages/device-config/index',
    text: '配网',
    icon: 'i-carbon-network-3',
    iconType: 'uiLib',
  },
  {
    iconPath: 'static/tabbar/system.png',
    selectedIconPath: 'static/tabbar/system_activate.png',
    pagePath: 'pages/settings/index',
    text: '系统',
    icon: 'i-carbon-settings',
    iconType: 'uiLib',
  },
]

// NATIVE_TABBAR(1) and CUSTOM_TABBAR_WITH_CACHE(2) hour，requires_tabbar_caching
export const cacheTabbarEnable = selectedTabbarStrategy === TABBAR_MAP.NATIVE_TABBAR
  || selectedTabbarStrategy === TABBAR_MAP.CUSTOM_TABBAR_WITH_CACHE

const _tabbar: TabBar = {
  // only_supported_by_wechat_mini_program custom。App and H5 not_effective
  custom: selectedTabbarStrategy === TABBAR_MAP.CUSTOM_TABBAR_WITH_CACHE,
  color: '#e6e6e6',
  selectedColor: '#667dea',
  backgroundColor: '#fff',
  borderStyle: 'black',
  height: '50px',
  fontSize: '10px',
  iconWidth: '24px',
  spacing: '3px',
  list: tabbarList as unknown as TabBar['list'],
}

// 0 and 1 various_configurations_of_the_tabbar_at_the_bottom_need_to_be_displayed, to_take_advantage_of_caching
export const tabBar = cacheTabbarEnable ? _tabbar : undefined
