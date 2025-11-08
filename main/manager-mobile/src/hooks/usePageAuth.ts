import { onLoad } from '@dcloudio/uni-app'
import { useUserStore } from '@/store'
import { needLoginPages as _needLoginPages, getNeedLoginPages } from '@/utils'

const loginRoute = import.meta.env.VITE_LOGIN_URL
const isDev = import.meta.env.DEV
function isLogined() {
  const userStore = useUserStore()
  return !!userStore.userInfo.username
}
// check_whether_the_current_page_requires_login
export function usePageAuth() {
  onLoad((options) => {
    // get_current_page_path
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    const currentPath = `/${currentPage.route}`

    // get_the_list_of_pages_that_require_login
    let needLoginPages: string[] = []
    if (isDev) {
      needLoginPages = getNeedLoginPages()
    }
    else {
      needLoginPages = _needLoginPages
    }

    // check_whether_the_current_page_requires_login
    const isNeedLogin = needLoginPages.includes(currentPath)
    if (!isNeedLogin) {
      return
    }

    const hasLogin = isLogined()
    if (hasLogin) {
      return true
    }

    // build_redirect_url
    const queryString = Object.entries(options || {})
      .map(([key, value]) => `${key}=${encodeURIComponent(String(value))}`)
      .join('&')

    const currentFullPath = queryString ? `${currentPath}?${queryString}` : currentPath
    const redirectRoute = `${loginRoute}?redirect=${encodeURIComponent(currentFullPath)}`

    // redirect_to_login_page
    uni.redirectTo({ url: redirectRoute })
  })
}
