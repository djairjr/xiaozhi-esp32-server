// requests_to_introduce_each_module
import admin from './module/admin.js'
import agent from './module/agent.js'
import device from './module/device.js'
import dict from './module/dict.js'
import model from './module/model.js'
import ota from './module/ota.js'
import timbre from "./module/timbre.js"
import user from './module/user.js'
import voiceClone from './module/voiceClone.js'
import voiceResource from './module/voiceResource.js'



/*
*
 * interface_address
* automatically_read_and_use_during_development.env.development file
* automatically_read_and_use_when_compiling.env.production file
*/
const DEV_API_SERVICE = process.env.VUE_APP_API_BASE_URL

/**
 * return_the_interface_url_according_to_the_development_environment
 * @returns {string}
 */
export function getServiceUrl() {
    return DEV_API_SERVICE
}

/* * request service encapsulation */
export default {
    getServiceUrl,
    user,
    admin,
    agent,
    device,
    model,
    timbre,
    ota,
    dict,
    voiceResource,
    voiceClone
}
