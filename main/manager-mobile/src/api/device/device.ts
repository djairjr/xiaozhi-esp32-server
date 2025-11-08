import type { Device, FirmwareType } from './types'
import { http } from '@/http/request/alova'

/**
 * get_a_list_of_device_types
 */
export function getFirmwareTypes() {
  return http.Get<FirmwareType[]>('/admin/dict/data/type/FIRMWARE_TYPE')
}

/**
 * get_the_list_of_bound_devices
 * @param agentId agent_id
 */
export function getBindDevices(agentId: string) {
  return http.Get<Device[]>(`/device/bind/${agentId}`, {
    meta: {
      ignoreAuth: false,
      toast: false,
    },
    cacheFor: {
      expire: 0,
    },
  })
}

/**
 * add_device
 * @param agentId agent_id
 * @param code verification_code
 */
export function bindDevice(agentId: string, code: string) {
  return http.Post(`/device/bind/${agentId}/${code}`, null)
}

/*
*
 * set_the_device_ota_upgrade_switch
* @param deviceId device_id (MAC address)
 * @param autoUpdate whether_to_automatically_upgrade 0|1
*/
export function updateDeviceAutoUpdate(deviceId: string, autoUpdate: number) {
  return http.Put(`/device/update/${deviceId}`, {
    autoUpdate,
  })
}

/*
*
 * unbind_device
* @param deviceId device_id (MAC address)
*/
export function unbindDevice(deviceId: string) {
  return http.Post('/device/unbind', {
    deviceId,
  })
}
