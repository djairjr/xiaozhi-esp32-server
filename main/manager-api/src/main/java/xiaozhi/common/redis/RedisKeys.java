package xiaozhi.common.redis;

/**
 * Redis Key constant_class
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
public class RedisKeys {
    /**
     * system_parameterkey
     */
    public static String getSysParamsKey() {
        return "sys:params";
    }

    /**
     * verification_codekey
     */
    public static String getCaptchaKey(String uuid) {
        return "sys:captcha:" + uuid;
    }

    /**
     * unregistered_device_verification_code_key
     */
    public static String getDeviceCaptchaKey(String captcha) {
        return "sys:device:captcha:" + captcha;
    }

    /**
     * key_of_user_id
     */
    public static String getUserIdKey(Long userid) {
        return "sys:username:id:" + userid;
    }

    /**
     * key_of_model_name
     */
    public static String getModelNameById(String id) {
        return "model:name:" + id;
    }

    /**
     * key_of_model_configuration
     */
    public static String getModelConfigById(String id) {
        return "model:data:" + id;
    }

    /**
     * get_the_timbre_name_cache_key
     */
    public static String getTimbreNameById(String id) {
        return "timbre:name:" + id;
    }

    /**
     * get_the_device_number_cache_key
     */
    public static String getAgentDeviceCountById(String id) {
        return "agent:device:count:" + id;
    }

    /**
     * get_the_agents_last_connection_time_cache_key
     */
    public static String getAgentDeviceLastConnectedAtById(String id) {
        return "agent:device:lastConnected:" + id;
    }

    /**
     * get_the_system_configuration_cache_key
     */
    public static String getServerConfigKey() {
        return "server:config";
    }

    /**
     * get_the_timbre_details_cache_key
     */
    public static String getTimbreDetailsKey(String id) {
        return "timbre:details:" + id;
    }

    /**
     * get_version_number_key
     */
    public static String getVersionKey() {
        return "sys:version";
    }

    /*
*
*Key of OTA firmware ID
*/
    public static String getOtaIdKey(String uuid) {
        return "ota:id:" + uuid;
    }

    /*
*
*Key of OTA firmware download times
*/
    public static String getOtaDownloadCountKey(String uuid) {
        return "ota:download:count:" + uuid;
    }

    /**
     * get_the_cache_key_of_dictionary_data
     */
    public static String getDictDataByTypeKey(String dictType) {
        return "sys:dict:data:" + dictType;
    }

    /**
     * get_the_cache_key_of_the_agent_audio_id
     */
    public static String getAgentAudioIdKey(String uuid) {
        return "agent:audio:id:" + uuid;
    }

    /**
     * get_the_cache_key_of_sms_verification_code
     */
    public static String getSMSValidateCodeKey(String phone) {
        return "sms:Validate:Code:" + phone;
    }

    /**
     * get_the_cache_key_of_the_last_time_the_sms_verification_code_was_sent
     */
    public static String getSMSLastSendTimeKey(String phone) {
        return "sms:Validate:Code:" + phone + ":last_send_time";
    }

    /**
     * get_the_cache_key_of_the_number_of_sms_verification_codes_sent_today
     */
    public static String getSMSTodayCountKey(String phone) {
        return "sms:Validate:Code:" + phone + ":today_count";
    }

    /**
     * key_of_chat_record_uuid_mapping
     */
    public static String getChatHistoryKey(String uuid) {
        return "agent:chat:history:" + uuid;
    }

    /**
     * get_the_cache_key_of_the_timbre_clone_audio_id
     */
    public static String getVoiceCloneAudioIdKey(String uuid) {
        return "voiceClone:audio:id:" + uuid;
    }
}
