/**
 * by feige on 2024-03-06
 * route_interception，usually_login_blocking
 * routing_whitelist_can_be_set，or_blacklist，which_one_to_choose_depends_on_your_business_needs
 * i_think_most_of_the_people_here_can_enter_freely，so_use_blacklist
 */
import { useUserStore } from '@/store'
import { needLoginPages as _needLoginPages, getLastPage, getNeedLoginPages } from '@/utils'

// TODO Check
const loginRoute = import.meta.env.VITE_LOGIN_URL

function isLogined() {
  const userStore = useUserStore()
  return !!userStore.userInfo.username
}

const isDev = import.meta.env.DEV

// blacklist_login_blocker - （applicable_to_most_pages_and_does_not_require_login，a_few_pages_require_login）
const navigateToInterceptor = {
  // notice, the URL here starts with '/', such as '/pages/index/index', which is different from the path in 'pages.json'
  // add_handling_of_relative_paths，BY netizen @ideal
  invoke({ url }: { url: string }) {
    // console.log(url) // /pages/route-interceptor/index?name=feige&age=30
    let path = url.split('?')[0]
    console.log('页面变动')

    // handling_relative_paths
    if (!path.startsWith('/')) {
      const currentPath = getLastPage().route
      const normalizedCurrentPath = currentPath.startsWith('/') ? currentPath : `/${currentPath}`
      const baseDir = normalizedCurrentPath.substring(0, normalizedCurrentPath.lastIndexOf('/'))
      path = `${baseDir}/${path}`
    }

    let needLoginPages: string[] = []
    // in_order_to_prevent_bugs_from_occurring_during_development，get_it_here_every_time。production_environment_can_be_moved_outside_the_function，better_performance
    if (isDev) {
      needLoginPages = getNeedLoginPages()
    }
    else {
      needLoginPages = _needLoginPages
    }
    const isNeedLogin = needLoginPages.includes(path)
    if (!isNeedLogin) {
      return true
    }
    const hasLogin = isLogined()
    if (hasLogin) {
      return true
    }
    const redirectRoute = `${loginRoute}?redirect=${encodeURIComponent(url)}`
    uni.navigateTo({ url: redirectRoute })
    return false
  },
}

export const routeInterceptor = {
  install() {
    uni.addInterceptor('navigateTo', navigateToInterceptor)
    uni.addInterceptor('reLaunch', navigateToInterceptor)
    uni.addInterceptor('redirectTo', navigateToInterceptor)
    uni.addInterceptor('switchTab', navigateToInterceptor)
  },
}
