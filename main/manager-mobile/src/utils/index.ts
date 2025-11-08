import { pages, subPackages } from '@/pages.json'
import { isMpWeixin } from './platform'

/**
 * runtime_server_address_overrides_storage_key
 */
export const SERVER_BASE_URL_OVERRIDE_KEY = 'server_base_url_override'

/**
 * set_up/clear/get server_address_overridden_at_runtime
 */
export function setServerBaseUrlOverride(url: string) {
  uni.setStorageSync(SERVER_BASE_URL_OVERRIDE_KEY, url)
}

export function clearServerBaseUrlOverride() {
  uni.removeStorageSync(SERVER_BASE_URL_OVERRIDE_KEY)
}

export function getServerBaseUrlOverride(): string | null {
  const value = uni.getStorageSync(SERVER_BASE_URL_OVERRIDE_KEY)
  return value || null
}

export function getLastPage() {
  // getCurrentPages() has_at_least_1_element，so_no_additional_judgment_will_be_made
  // const lastPage = getCurrentPages().at(-1)
  // the_above_one_will_report_an_error_when_packaged_in_a_lower_version_of_android，so_use_the_following_instead【although_i_added src/interceptions/prototype.ts，but_still_reporting_an_error】
  const pages = getCurrentPages()
  return pages[pages.length - 1]
}

/*
*
 * get_the_route_of_the_current_page path path_and redirectPath path
* path such as '/pages/login/index'
* redirectPath such as '/pages/demo/base/route-interceptor'
*/
export function currRoute() {
  const lastPage = getLastPage()
  const currRoute = (lastPage as any).$page
  // console.log('lastPage.$page:', currRoute)
  // console.log('lastPage.$page.fullpath:', currRoute.fullPath)
  // console.log('lastPage.$page.options:', currRoute.options)
  // console.log('lastPage.options:', (lastPage as any).options)
  // after_multiterminal_testing，only fullPath reliable，others_are_unreliable
  const { fullPath } = currRoute as { fullPath: string }
  // console.log(fullPath)
  // eg: /pages/login/index?redirect=%2Fpages%2Fdemo%2Fbase%2Froute-interceptor (mini_program)
  // eg: /pages/login/index?redirect=%2Fpages%2Froute-interceptor%2Findex%3Fname%3Dfeige%26age%3D30(h5)
  return getUrlObj(fullPath)
}

function ensureDecodeURIComponent(url: string) {
  if (url.startsWith('%')) {
    return ensureDecodeURIComponent(decodeURIComponent(url))
  }
  return url
}
/**
 * parse url get path and query
 * for_example_enter_the_url: /pages/login/index?redirect=%2Fpages%2Fdemo%2Fbase%2Froute-interceptor
 * output: {path: /pages/login/index, query: {redirect: /pages/demo/base/route-interceptor}}
 */
export function getUrlObj(url: string) {
  const [path, queryStr] = url.split('?')
  // console.log(path, queryStr)

  if (!queryStr) {
    return {
      path,
      query: {},
    }
  }
  const query: Record<string, string> = {}
  queryStr.split('&').forEach((item) => {
    const [key, value] = item.split('=')
    // console.log(key, value)
    query[key] = ensureDecodeURIComponent(value) // need_to_unify_here decodeURIComponent one_time，compatible_with_h5_and_wechat_y
  })
  return { path, query }
}
/**
 * get_all_the_required_logins pages，including_main_package_and_subcontract
 * designed_here_to_be_more_general，can_be_delivered key as_a_basis_for_judgment，the_default_is needLogin, and route-block use_in_pairs
 * if_not_passed key，means_all pages，if_passed key, means_passing key filter
 */
export function getAllPages(key = 'needLogin') {
  // the_main_package_is_processed_here
  const mainPages = pages
    .filter(page => !key || page[key])
    .map(page => ({
      ...page,
      path: `/${page.path}`,
    }))

  // subcontracting_is_handled_here
  const subPages: any[] = []
  subPackages.forEach((subPageObj) => {
    // console.log(subPageObj)
    const { root } = subPageObj

    subPageObj.pages
      .filter(page => !key || page[key])
      .forEach((page: { path: string } & Record<string, any>) => {
        subPages.push({
          ...page,
          path: `/${root}/${page.path}`,
        })
      })
  })
  const result = [...mainPages, ...subPages]
  // console.log(`getAllPages by ${key} result: `, result)
  return result
}

/**
 * get_all_the_required_logins pages，including_main_package_and_subcontract
 * only_get path array
 */
export const getNeedLoginPages = (): string[] => getAllPages('needLogin').map(page => page.path)

/**
 * get_all_the_required_logins pages，including_main_package_and_subcontract
 * only_get path array
 */
export const needLoginPages: string[] = getAllPages('needLogin').map(page => page.path)

/**
 * according_to_the_current_environment_of_wechat_applet，determine_what_should_be_obtained baseUrl
 */
export function getEnvBaseUrl() {
  // if_there_is_an_override_address_set_by_the_user，return_first
  const override = getServerBaseUrlOverride()
  if (override)
    return override

  // request_base_address（the_default_source_is env）
  let baseUrl = import.meta.env.VITE_SERVER_BASEURL

  // # some_students_may_need_to_follow_the_instructions_in_the_wechat_applet develop、trial、release set_the_upload_address_separately，the_reference_code_is_as_follows。
  const VITE_SERVER_BASEURL__WEIXIN_DEVELOP = 'https://ukw0y1.laf.run'
  const VITE_SERVER_BASEURL__WEIXIN_TRIAL = 'https://ukw0y1.laf.run'
  const VITE_SERVER_BASEURL__WEIXIN_RELEASE = 'https://ukw0y1.laf.run'

  // wechat_applet_environment_distinction
  if (isMpWeixin) {
    const {
      miniProgram: { envVersion },
    } = uni.getAccountInfoSync()

    switch (envVersion) {
      case 'develop':
        baseUrl = VITE_SERVER_BASEURL__WEIXIN_DEVELOP || baseUrl
        break
      case 'trial':
        baseUrl = VITE_SERVER_BASEURL__WEIXIN_TRIAL || baseUrl
        break
      case 'release':
        baseUrl = VITE_SERVER_BASEURL__WEIXIN_RELEASE || baseUrl
        break
    }
  }

  return baseUrl
}

/**
 * according_to_the_current_environment_of_wechat_applet，determine_what_should_be_obtained UPLOAD_BASEURL
 */
export function getEnvBaseUploadUrl() {
  // request_base_address
  let baseUploadUrl = import.meta.env.VITE_UPLOAD_BASEURL

  const VITE_UPLOAD_BASEURL__WEIXIN_DEVELOP = 'https://ukw0y1.laf.run/upload'
  const VITE_UPLOAD_BASEURL__WEIXIN_TRIAL = 'https://ukw0y1.laf.run/upload'
  const VITE_UPLOAD_BASEURL__WEIXIN_RELEASE = 'https://ukw0y1.laf.run/upload'

  // wechat_applet_environment_distinction
  if (isMpWeixin) {
    const {
      miniProgram: { envVersion },
    } = uni.getAccountInfoSync()

    switch (envVersion) {
      case 'develop':
        baseUploadUrl = VITE_UPLOAD_BASEURL__WEIXIN_DEVELOP || baseUploadUrl
        break
      case 'trial':
        baseUploadUrl = VITE_UPLOAD_BASEURL__WEIXIN_TRIAL || baseUploadUrl
        break
      case 'release':
        baseUploadUrl = VITE_UPLOAD_BASEURL__WEIXIN_RELEASE || baseUploadUrl
        break
    }
  }

  return baseUploadUrl
}

import smCrypto from 'sm-crypto'

/**
 * generate_sm2_key_pair（hexadecimal_format）
 * @returns {Object} object_containing_public_and_private_keys
 */
export function generateSm2KeyPairHex() {
    // use_sm-crypto library generates SM2 key pairs
    const sm2 = smCrypto.sm2;
    const keypair = sm2.generateKeyPairHex();
    
    return {
        publicKey: keypair.publicKey,
        privateKey: keypair.privateKey,
        clientPublicKey: keypair.publicKey, // client_public_key
        clientPrivateKey: keypair.privateKey // client_private_key
    };
}

/*
*
* SM2 public key encryption
 * @param {string} publicKey public_key（hexadecimal_format）
 * @param {string} plainText plain_text
 * @returns {string} encrypted_ciphertext（hexadecimal_format）
*/
export function sm2Encrypt(publicKey: string, plainText: string): string {
    if (!publicKey) {
        throw new Error('公钥不能为null或undefined');
    }
    
    if (!plainText) {
        throw new Error('明文不能为空');
    }
    
    const sm2 = smCrypto.sm2;
    // SM2 encryption, add_04_prefix_to_indicate_uncompressed_public_key
    const encrypted = sm2.doEncrypt(plainText, publicKey, 1);
    // convert_to_hexadecimal_format（be_consistent_with_the_backend，add_04_prefix）
    const result = "04" + encrypted;
    
    return result;
}

/*
*
* SM2 private key decryption
 * @param {string} privateKey private_key（hexadecimal_format）
 * @param {string} cipherText cipher_text（hexadecimal_format）
 * @returns {string} decrypted_plaintext
*/
export function sm2Decrypt(privateKey: string, cipherText: string): string {
    const sm2 = smCrypto.sm2;
    // remove_04_prefix（be_consistent_with_the_backend）
    const dataWithoutPrefix = cipherText.startsWith("04") ? cipherText.substring(2) : cipherText;
    // SM2 decryption
    return sm2.doDecrypt(dataWithoutPrefix, privateKey, 1);
}
