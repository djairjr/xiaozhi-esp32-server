import type { uniappRequestAdapter } from '@alova/adapter-uniapp'
import type { IResponse } from './types'
import AdapterUniapp from '@alova/adapter-uniapp'
import { createAlova } from 'alova'
import { createServerTokenAuthentication } from 'alova/client'
import VueHook from 'alova/vue'
import { getEnvBaseUrl } from '@/utils'
import { toast } from '@/utils/toast'
import { ContentTypeEnum, ResultEnum, ShowMessage } from './enum'

/**
 * create_request_instance
 */
const { onAuthRequired, onResponseRefreshToken } = createServerTokenAuthentication<
  typeof VueHook,
  typeof uniappRequestAdapter
>({
  refreshTokenOnError: {
    isExpired: (error) => {
      return error.response?.status === ResultEnum.Unauthorized
    },
    handler: async () => {
      try {
        // await authLogin();
      }
      catch (error) {
        // switch_to_login_page
        await uni.reLaunch({ url: '/pages/login/index' })
        throw error
      }
    },
  },
})

/**
 * alova request_instance
 */
const alovaInstance = createAlova({
  baseURL: getEnvBaseUrl(),
  ...AdapterUniapp(),
  timeout: 5000,
  statesHook: VueHook,

  beforeRequest: onAuthRequired((method) => {
    // set_default Content-Type
    method.config.headers = {
      'Content-Type': ContentTypeEnum.JSON,
      'Accept': 'application/json, text/plain, */*',
      ...method.config.headers,
    }

    const { config } = method
    const ignoreAuth = config.meta?.ignoreAuth
    console.log('ignoreAuth===>', ignoreAuth)

    // process_authentication_information
    if (!ignoreAuth) {
      const token = uni.getStorageSync('token')
      if (!token) {
        // jump_to_login_page
        uni.reLaunch({ url: '/pages/login/index' })
        throw new Error('[请求错误]：未登录')
      }
      // add_to Authorization head
      method.config.headers.Authorization = `Bearer ${token}`
    }

    // handling_dynamic_domain_names
    if (config.meta?.domain) {
      method.baseURL = config.meta.domain
      console.log('当前域名', method.baseURL)
    }
  }),

  responded: onResponseRefreshToken((response, method) => {
    const { config } = method
    const { requestType } = config
    const {
      statusCode,
      data: rawData,
      errMsg,
    } = response as UniNamespace.RequestSuccessCallbackResult

    console.log(response)

    // handle_special_request_types（upload/download）
    if (requestType === 'upload' || requestType === 'download') {
      return response
    }

    // deal_with HTTP status_code_error
    if (statusCode !== 200) {
      const errorMessage = ShowMessage(statusCode) || `HTTP请求错误[${statusCode}]`
      console.error('errorMessage===>', errorMessage)
      toast.error(errorMessage)
      throw new Error(`${errorMessage}：${errMsg}`)
    }

    // handle_business_logic_errors
    const { code, msg, data } = rawData as IResponse
    if (code !== ResultEnum.Success) {
      // check_whether_the_token_is_invalid
      if (code === ResultEnum.Unauthorized) {
        // clear_token_and_jump_to_login_page
        uni.removeStorageSync('token')
        uni.reLaunch({ url: '/pages/login/index' })
        throw new Error(`request_error[${code}]：${msg}`)
      }

      if (config.meta?.toast !== false) {
        toast.warning(msg)
      }
      throw new Error(`request_error[${code}]：${msg}`)
    }
    // handle_successful_response，return_business_data
    return data
  }),
})

export const http = alovaInstance
