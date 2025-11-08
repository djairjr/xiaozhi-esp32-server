export enum ResultEnum {
  Success = 0, // success
  Error = 400, // mistake
  Unauthorized = 401, // unauthorized
  Forbidden = 403, // forbidden_access（formerly_forbidden）
  NotFound = 404, // not_found（was_notfound）
  MethodNotAllowed = 405, // method_not_allowed（was_methodnotallowed）
  RequestTimeout = 408, // request_timeout（originally_requesttimeout）
  InternalServerError = 500, // server_error（was_internalservererror）
  NotImplemented = 501, // not_implemented（was_notimplemented）
  BadGateway = 502, // gateway_error（formerly_badgateway）
  ServiceUnavailable = 503, // service_is_unavailable（was_serviceunavailable）
  GatewayTimeout = 504, // gateway_timeout（originally_gatewaytimeout）
  HttpVersionNotSupported = 505, // HTTP version is not supported (was_httpversionnotsupported)
}
export enum ContentTypeEnum {
  JSON = 'application/json;charset=UTF-8',
  FORM_URLENCODED = 'application/x-www-form-urlencoded;charset=UTF-8',
  FORM_DATA = 'multipart/form-data;charset=UTF-8',
}
/**
 * according_to_status_code，generate_corresponding_error_message
 * @param {number|string} status status_code
 * @returns {string} error_message
 */
export function ShowMessage(status: number | string): string {
  let message: string
  switch (status) {
    case 400:
      message = '请求错误(400)'
      break
    case 401:
      message = '未授权，please_log_in_again(401)'
      break
    case 403:
      message = '拒绝访问(403)'
      break
    case 404:
      message = '请求出错(404)'
      break
    case 408:
      message = '请求超时(408)'
      break
    case 500:
      message = '服务器错误(500)'
      break
    case 501:
      message = '服务未实现(501)'
      break
    case 502:
      message = '网络错误(502)'
      break
    case 503:
      message = '服务不可用(503)'
      break
    case 504:
      message = '网络超时(504)'
      break
    case 505:
      message = 'HTTP版本不受支持(505)'
      break
    default:
      message = `connection_error(${status})!`
  }
  return `${message}，please_check_the_network_or_contact_the_administrator！`
}
