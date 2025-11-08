import { Message } from 'element-ui'
import router from '../router'
import Constant from '../utils/constant'

/**
 * determine_whether_the_user_is_logged_in
 */
export function checkUserLogin(fn) {
    let token = localStorage.getItem(Constant.STORAGE_KEY.TOKEN)
    let userType = localStorage.getItem(Constant.STORAGE_KEY.USER_TYPE)
    if (isNull(token) || isNull(userType)) {
        goToPage('console', true)
        return
    }
    if (fn) {
        fn()
    }
}

/**
 * determine_whether_it_is_empty
 * @param data
 * @returns {boolean}
 */
export function isNull(data) {
    if (data === undefined) {
        return true
    } else if (data === null) {
        return true
    } else if (typeof data === 'string' && (data.length === 0 || data === '' || data === 'undefined' || data === 'null')) {
        return true
    } else if ((data instanceof Array) && data.length === 0) {
        return true
    }
    return false
}

/**
 * judgment_is_not_empty
 * @param data
 * @returns {boolean}
 */
export function isNotNull(data) {
    return !isNull(data)
}

/**
 * show_top_red_notification
 * @param msg
 */
export function showDanger(msg) {
    if (isNull(msg)) {
        return
    }
    Message({
        message: msg,
        type: 'error',
        showClose: true
    })
}

/**
 * show_top_orange_notification
 * @param msg
 */
export function showWarning(msg) {
    if (isNull(msg)) {
        return
    }
    Message({
        message: msg,
        type: 'warning',
        showClose: true
    });
}



/**
 * show_top_green_notification
 * @param msg
 */
export function showSuccess(msg) {
    Message({
        message: msg,
        type: 'success',
        showClose: true
    })
}



/**
 * page_jump
 * @param path
 * @param isRepalce
 */
export function goToPage(path, isRepalce) {
    if (isRepalce) {
        router.replace(path)
    } else {
        router.push(path)
    }
}

/**
 * get_the_current_vue_page_name
 * @param path
 * @param isRepalce
 */
export function getCurrentPage() {
    let hash = location.hash.replace('#', '')
    if (hash.indexOf('?') > 0) {
        hash = hash.substring(0, hash.indexOf('?'))
    }
    return hash
}

/**
 * generated_from[min,max]random_number
 * @param min
 * @param max
 * @returns {number}
 */
export function randomNum(min, max) {
    return Math.round(Math.random() * (max - min) + min)
}


/**
 * get_uuid
 */
export function getUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
        return (c === 'x' ? (Math.random() * 16 | 0) : ('r&0x3' | '0x8')).toString(16)
    })
}


/**
 * verify_mobile_phone_number_format
 * @param {string} mobile phone_number
 * @param {string} areaCode area_code
 * @returns {boolean}
 */
export function validateMobile(mobile, areaCode) {
    // remove_all_nonnumeric_characters
    const cleanMobile = mobile.replace(/\D/g, '');

    // use_different_validation_rules_based_on_different_area_codes
    switch (areaCode) {
        case '+86': // chinese_mainland
            return /^1[3-9]\d{9}$/.test(cleanMobile);
        case '+852': // hong_kong_china
            return /^[569]\d{7}$/.test(cleanMobile);
        case '+853': // macau_china
            return /^6\d{7}$/.test(cleanMobile);
        case '+886': // taiwan_china
            return /^9\d{8}$/.test(cleanMobile);
        case '+1': // usa/canada
            return /^[2-9]\d{9}$/.test(cleanMobile);
        case '+44': // uk
            return /^7[1-9]\d{8}$/.test(cleanMobile);
        case '+81': // japan
            return /^[7890]\d{8}$/.test(cleanMobile);
        case '+82': // south_korea
            return /^1[0-9]\d{7}$/.test(cleanMobile);
        case '+65': // singapore
            return /^[89]\d{7}$/.test(cleanMobile);
        case '+61': // australia
            return /^[4578]\d{8}$/.test(cleanMobile);
        case '+49': // germany
            return /^1[5-7]\d{8}$/.test(cleanMobile);
        case '+33': // france
            return /^[67]\d{8}$/.test(cleanMobile);
        case '+39': // italy
            return /^3[0-9]\d{8}$/.test(cleanMobile);
        case '+34': // spain
            return /^[6-9]\d{8}$/.test(cleanMobile);
        case '+55': // brazil
            return /^[1-9]\d{10}$/.test(cleanMobile);
        case '+91': // india
            return /^[6-9]\d{9}$/.test(cleanMobile);
        case '+971': // united_arab_emirates
            return /^[5]\d{8}$/.test(cleanMobile);
        case '+966': // saudi_arabia
            return /^[5]\d{8}$/.test(cleanMobile);
        case '+880': // bangladesh
            return /^1[3-9]\d{8}$/.test(cleanMobile);
        case '+234': // nigeria
            return /^[789]\d{9}$/.test(cleanMobile);
        case '+254': // kenya
            return /^[17]\d{8}$/.test(cleanMobile);
        case '+255': // tanzania
            return /^[67]\d{8}$/.test(cleanMobile);
        case '+7': // kazakhstan
            return /^[67]\d{9}$/.test(cleanMobile);
        default:
            // other_international_numbers：at_least_5_people，maximum_15_people
            return /^\d{5,15}$/.test(cleanMobile);
    }
}


/**
 * generate_sm2_key_pair（hexadecimal_format）
 * @returns {Object} object_containing_public_and_private_keys
 */
export function generateSm2KeyPairHex() {
    // use_sm-crypto library generates SM2 key pairs
    const sm2 = require('sm-crypto').sm2;
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
export function sm2Encrypt(publicKey, plainText) {
    if (!publicKey) {
        throw new Error('公钥不能为null或undefined');
    }
    
    if (!plainText) {
        throw new Error('明文不能为空');
    }
    
    const sm2 = require('sm-crypto').sm2;
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
export function sm2Decrypt(privateKey, cipherText) {
    const sm2 = require('sm-crypto').sm2;
    // remove_04_prefix（be_consistent_with_the_backend）
    const dataWithoutPrefix = cipherText.startsWith("04") ? cipherText.substring(2) : cipherText;
    // SM2 decryption
    return sm2.doDecrypt(dataWithoutPrefix, privateKey, 1);
}

