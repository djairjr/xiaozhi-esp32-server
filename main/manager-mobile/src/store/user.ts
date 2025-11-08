import type { UserInfo } from '@/api/auth'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  getUserInfo as _getUserInfo,
} from '@/api/auth'

// initialization_state
const userInfoState: UserInfo & { avatar?: string, token?: string } = {
  id: 0,
  username: '',
  realName: '',
  email: '',
  mobile: '',
  status: 0,
  superAdmin: 0,
  avatar: '/static/images/default-avatar.png',
  token: '',
}

export const useUserStore = defineStore(
  'user',
  () => {
    // define_user_information
    const userInfo = ref<UserInfo & { avatar?: string, token?: string }>({ ...userInfoState })
    // set_user_information
    const setUserInfo = (val: UserInfo & { avatar?: string, token?: string }) => {
      console.log('设置用户信息', val)
      // if_the_avatar_is_empty then_use_the_default_avatar
      if (!val.avatar) {
        val.avatar = userInfoState.avatar
      }
      else {
        val.avatar = 'https://oss.laf.run/ukw0y1-site/avatar.jpg?feige'
      }
      userInfo.value = val
    }
    const setUserAvatar = (avatar: string) => {
      userInfo.value.avatar = avatar
      console.log('设置用户头像', avatar)
      console.log('userInfo', userInfo.value)
    }
    // delete_user_information
    const removeUserInfo = () => {
      userInfo.value = { ...userInfoState }
      uni.removeStorageSync('userInfo')
      uni.removeStorageSync('token')
    }
    /**
     * get_user_information
     */
    const getUserInfo = async () => {
      const userData = await _getUserInfo()
      const userInfoWithExtras = {
        ...userData,
        avatar: userInfoState.avatar,
        token: uni.getStorageSync('token') || '',
      }
      setUserInfo(userInfoWithExtras)
      uni.setStorageSync('userInfo', userInfoWithExtras)
      // TODO here_you_can_add_a_method_to_obtain_user_routes dynamically_generate_routes_based_on_user_roles
      return userInfoWithExtras
    }
    /**
     * log_out and delete_user_information
     */
    const logout = async () => {
      removeUserInfo()
    }

    return {
      userInfo,
      getUserInfo,
      setUserInfo,
      setUserAvatar,
      logout,
      removeUserInfo,
    }
  },
  {
    persist: true,
  },
)
