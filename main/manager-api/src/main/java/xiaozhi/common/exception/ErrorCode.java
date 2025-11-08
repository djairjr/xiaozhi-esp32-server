package xiaozhi.common.exception;

/*
*
 * error_coding，consists_of_5_digits，the_first_2_digits_are_the_module_code，the_last_3_digits_are_the_business_code
 * <p>
* like: 10001 (10 represents system module, 001 represents business code)
 * </p>
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
*/
public interface ErrorCode {
    int INTERNAL_SERVER_ERROR = 500;
    int UNAUTHORIZED = 401;
    int FORBIDDEN = 403;

    int NOT_NULL = 10001;
    int DB_RECORD_EXISTS = 10002;
    int PARAMS_GET_ERROR = 10003;
    int ACCOUNT_PASSWORD_ERROR = 10004;
    int ACCOUNT_DISABLE = 10005;
    int IDENTIFIER_NOT_NULL = 10006;
    int CAPTCHA_ERROR = 10007;
    int PHONE_NOT_NULL = 10008;
    int PASSWORD_ERROR = 10009;

    int SUPERIOR_DEPT_ERROR = 10011;
    int SUPERIOR_MENU_ERROR = 10012;
    int DATA_SCOPE_PARAMS_ERROR = 10013;
    int DEPT_SUB_DELETE_ERROR = 10014;
    int DEPT_USER_DELETE_ERROR = 10015;

    int UPLOAD_FILE_EMPTY = 10019;
    int TOKEN_NOT_EMPTY = 10020;
    int TOKEN_INVALID = 10021;
    int ACCOUNT_LOCK = 10022;

    int OSS_UPLOAD_FILE_ERROR = 10024;

    int REDIS_ERROR = 10027;
    int JOB_ERROR = 10028;
    int INVALID_SYMBOL = 10029;
    int PASSWORD_LENGTH_ERROR = 10030;
    int PASSWORD_WEAK_ERROR = 10031;
    int DEL_MYSELF_ERROR = 10032;
    int DEVICE_CAPTCHA_ERROR = 10033;

    // parameter_verification_related_error_codes
    int PARAM_VALUE_NULL = 10034;
    int PARAM_TYPE_NULL = 10035;
    int PARAM_TYPE_INVALID = 10036;
    int PARAM_NUMBER_INVALID = 10037;
    int PARAM_BOOLEAN_INVALID = 10038;
    int PARAM_ARRAY_INVALID = 10039;
    int PARAM_JSON_INVALID = 10040;

    int OTA_DEVICE_NOT_FOUND = 10041;
    int OTA_DEVICE_NEED_BIND = 10042;

    // added_error_code
    int DELETE_DATA_FAILED = 10043;
    int USER_NOT_LOGIN = 10044;
    int WEB_SOCKET_CONNECT_FAILED = 10045;
    int VOICE_PRINT_SAVE_ERROR = 10046;
    int TODAY_SMS_LIMIT_REACHED = 10047;
    int OLD_PASSWORD_ERROR = 10048;
    int INVALID_LLM_TYPE = 10049;
    int TOKEN_GENERATE_ERROR = 10050;
    int RESOURCE_NOT_FOUND = 10051;

    // added_error_code
    int DEFAULT_AGENT_NOT_FOUND = 10052;
    int AGENT_NOT_FOUND = 10053;
    int VOICEPRINT_API_NOT_CONFIGURED = 10054;
    int SMS_SEND_FAILED = 10055;
    int SMS_CONNECTION_FAILED = 10056;
    int AGENT_VOICEPRINT_CREATE_FAILED = 10057;
    int AGENT_VOICEPRINT_UPDATE_FAILED = 10058;
    int AGENT_VOICEPRINT_DELETE_FAILED = 10059;
    int SMS_SEND_TOO_FREQUENTLY = 10060;
    int ACTIVATION_CODE_EMPTY = 10061;
    int ACTIVATION_CODE_ERROR = 10062;
    int DEVICE_ALREADY_ACTIVATED = 10063;
    // default_model_deletion_error
    int DEFAULT_MODEL_DELETE_ERROR = 10064;
    // login_related_error_codes
    int ADD_DATA_FAILED = 10065; // failed_to_add_data
    int UPDATE_DATA_FAILED = 10066; // failed_to_modify_data
    int SMS_CAPTCHA_ERROR = 10067; // sms_verification_code_error
    int MOBILE_REGISTER_DISABLED = 10068; // mobile_phone_registration_not_enabled
    int USERNAME_NOT_PHONE = 10069; // username_is_not_a_mobile_phone_number
    int PHONE_ALREADY_REGISTERED = 10070; // mobile_number_has_been_registered
    int PHONE_NOT_REGISTERED = 10071; // mobile_number_is_not_registered
    int USER_REGISTER_DISABLED = 10072; // user_registration_is_not_allowed
    int RETRIEVE_PASSWORD_DISABLED = 10073; // password_retrieval_function_is_not_enabled
    int PHONE_FORMAT_ERROR = 10074; // mobile_phone_number_format_is_incorrect
    int SMS_CODE_ERROR = 10075; // mobile_phone_verification_code_error

    // dictionary_type_related_error_codes
    int DICT_TYPE_NOT_EXIST = 10076; // dictionary_type_does_not_exist
    int DICT_TYPE_DUPLICATE = 10077; // dictionary_type_encoding_duplicate

    // resource_processing_related_error_codes
    int RESOURCE_READ_ERROR = 10078; // failed_to_read_resource

    // agent_related_error_codes
    int LLM_INTENT_PARAMS_MISMATCH = 10079; // LLM large model and Intent intent recognition, selection_parameters_do_not_match

    // voiceprint_related_error_codes
    int VOICEPRINT_ALREADY_REGISTERED = 10080; // this_voiceprint_has_already_been_registered
    int VOICEPRINT_DELETE_ERROR = 10081; // an_error_occurred_while_deleting_voiceprint
    int VOICEPRINT_UPDATE_NOT_ALLOWED = 10082; // voiceprint_modification_is_not_allowed，sound_is_registered
    int VOICEPRINT_UPDATE_ADMIN_ERROR = 10083; // fix_voiceprint_errors，please_contact_the_administrator
    int VOICEPRINT_API_URI_ERROR = 10084; // voiceprint_interface_address_error
    int VOICEPRINT_AUDIO_NOT_BELONG_AGENT = 10085; // audio_data_does_not_belong_to_the_agent
    int VOICEPRINT_AUDIO_EMPTY = 10086; // audio_data_is_empty
    int VOICEPRINT_REGISTER_REQUEST_ERROR = 10087; // voiceprint_save_request_failed
    int VOICEPRINT_REGISTER_PROCESS_ERROR = 10088; // voiceprint_saving_process_failed
    int VOICEPRINT_UNREGISTER_REQUEST_ERROR = 10089; // voiceprint_logout_request_failed
    int VOICEPRINT_UNREGISTER_PROCESS_ERROR = 10090; // voiceprint_logout_processing_failed
    int VOICEPRINT_IDENTIFY_REQUEST_ERROR = 10091; // voiceprint_recognition_request_failed

    // device_related_error_codes
    int MAC_ADDRESS_ALREADY_EXISTS = 10161; // Mac address already exists
    // model_related_error_codes
    int MODEL_PROVIDER_NOT_EXIST = 10162; // provider_does_not_exist
    int LLM_NOT_EXIST = 10092; // the_set_llm_does_not_exist
    int MODEL_REFERENCED_BY_AGENT = 10093; // the_model_configuration_has_been_referenced_by_the_agent，cannot_be_deleted
    int LLM_REFERENCED_BY_INTENT = 10094; // this_llm_model_has_been_referenced_by_the_intent_recognition_configuration，cannot_be_deleted

    // server_management_related_error_codes
    int INVALID_SERVER_ACTION = 10095; // invalid_server_operation
    int SERVER_WEBSOCKET_NOT_CONFIGURED = 10096; // the_server_websocket_address_is_not_configured
    int TARGET_WEBSOCKET_NOT_EXIST = 10097; // the_target_websocket_address_does_not_exist

    // parameter_verification_related_error_codes
    int WEBSOCKET_URLS_EMPTY = 10098; // WebSocket address list cannot be empty
    int WEBSOCKET_URL_LOCALHOST = 10099; // WebSocket addresses cannot use localhost or 127.0.0.1
    int WEBSOCKET_URL_FORMAT_ERROR = 10100; // WebSocket address format is incorrect
    int WEBSOCKET_CONNECTION_FAILED = 10101; // WebSocket connection test failed
    int OTA_URL_EMPTY = 10102; // OTA address cannot be empty
    int OTA_URL_LOCALHOST = 10103; // The OTA address cannot use localhost or 127.0.0.1
    int OTA_URL_PROTOCOL_ERROR = 10104; // OTA address must start with http or https
    int OTA_URL_FORMAT_ERROR = 10105; // The OTA address must end with /ota/ending
    int OTA_INTERFACE_ACCESS_FAILED = 10106; // OTA interface access failed
    int OTA_INTERFACE_FORMAT_ERROR = 10107; // The format of the content returned by the OTA interface is incorrect
    int OTA_INTERFACE_VALIDATION_FAILED = 10108; // OTA interface verification failed
    int MCP_URL_EMPTY = 10109; // MCP address cannot be empty
    int MCP_URL_LOCALHOST = 10110; // The MCP address cannot use localhost or 127.0.0.1
    int MCP_URL_INVALID = 10111; // not_the_correct_mcp_address
    int MCP_INTERFACE_ACCESS_FAILED = 10112; // MCP interface access failed
    int MCP_INTERFACE_FORMAT_ERROR = 10113; // The format of the content returned by the MCP interface is incorrect
    int MCP_INTERFACE_VALIDATION_FAILED = 10114; // MCP interface verification failed
    int VOICEPRINT_URL_EMPTY = 10115; // the_voiceprint_interface_address_cannot_be_empty
    int VOICEPRINT_URL_LOCALHOST = 10116; // the_voiceprint_interface_address_cannot_use_localhost_or_127.0.0.1
    int VOICEPRINT_URL_INVALID = 10117; // incorrect_voiceprint_interface_address
    int VOICEPRINT_URL_PROTOCOL_ERROR = 10118; // the_voiceprint_interface_address_must_start_with_http_or_https
    int VOICEPRINT_INTERFACE_ACCESS_FAILED = 10119; // voiceprint_interface_access_failed
    int VOICEPRINT_INTERFACE_FORMAT_ERROR = 10120; // the_content_format_returned_by_the_voiceprint_interface_is_incorrect
    int VOICEPRINT_INTERFACE_VALIDATION_FAILED = 10121; // voiceprint_interface_verification_failed
    int MQTT_SECRET_EMPTY = 10122; // mqtt key cannot be empty
    int MQTT_SECRET_LENGTH_INSECURE = 10123; // mqtt key length is not secure
    int MQTT_SECRET_CHARACTER_INSECURE = 10124; // mqtt key must contain both uppercase and lowercase letters
    int MQTT_SECRET_WEAK_PASSWORD = 10125; // mqtt key contains weak password
    int DICT_LABEL_DUPLICATE = 10128; // dictionary_tag_duplicate
    int SM2_KEY_NOT_CONFIGURED = 10129; // SM2 key not configured
    int SM2_DECRYPT_ERROR = 10130; // SM2 decryption failed
    int MODEL_TYPE_PROVIDE_CODE_NOT_NULL = 10131; // modelType and provideCode cannot be empty

    // chat_history_related_error_codes
    int CHAT_HISTORY_NO_PERMISSION = 10132; // no_permission_to_view_the_chat_history_of_this_agent
    int CHAT_HISTORY_SESSION_ID_NOT_NULL = 10133; // session_id_cannot_be_empty
    int CHAT_HISTORY_AGENT_ID_NOT_NULL = 10134; // agent_id_cannot_be_empty
    int CHAT_HISTORY_DOWNLOAD_FAILED = 10135; // chat_history_download_failed
    int DOWNLOAD_LINK_EXPIRED = 10136; // the_download_link_has_expired_or_is_invalid
    int DOWNLOAD_LINK_INVALID = 10137; // download_link_is_invalid
    int CHAT_ROLE_USER = 10138; // user_role
    int CHAT_ROLE_AGENT = 10139; // agent_role

    // sound_cloning_related_error_codes
    int VOICE_CLONE_AUDIO_EMPTY = 10140; // audio_file_cannot_be_empty
    int VOICE_CLONE_NOT_AUDIO_FILE = 10141; // only_supports_audio_files
    int VOICE_CLONE_AUDIO_TOO_LARGE = 10142; // audio_file_size_cannot_exceed_10mb
    int VOICE_CLONE_UPLOAD_FAILED = 10143; // upload_failed
    int VOICE_CLONE_RECORD_NOT_EXIST = 10144; // sound_clone_record_does_not_exist
    int VOICE_RESOURCE_INFO_EMPTY = 10145; // tone_resource_information_cannot_be_empty
    int VOICE_RESOURCE_PLATFORM_NAME_EMPTY = 10146; // platform_name_cannot_be_empty
    int VOICE_RESOURCE_ID_EMPTY = 10147; // tone_id_cannot_be_empty
    int VOICE_RESOURCE_ACCOUNT_EMPTY = 10148; // the_attributed_account_cannot_be_empty
    int VOICE_RESOURCE_DELETE_ID_EMPTY = 10149; // the_deleted_sound_resource_id_cannot_be_empty
    int VOICE_RESOURCE_NO_PERMISSION = 10150; // you_do_not_have_permission_to_operate_this_record
    int VOICE_CLONE_AUDIO_NOT_UPLOADED = 10151; // please_upload_the_audio_file_first
    int VOICE_CLONE_MODEL_CONFIG_NOT_FOUND = 10152; // model_configuration_not_found
    int VOICE_CLONE_MODEL_TYPE_NOT_FOUND = 10153; // model_type_not_found
    int VOICE_CLONE_TRAINING_FAILED = 10154; // training_failed
    int VOICE_CLONE_HUOSHAN_CONFIG_MISSING = 10155; // volcano_engine_missing_configuration
    int VOICE_CLONE_RESPONSE_FORMAT_ERROR = 10156; // response_format_error
    int VOICE_CLONE_REQUEST_FAILED = 10157; // request_failed
    int VOICE_CLONE_PREFIX = 10158; // replica_tone_prefix
    int VOICE_ID_ALREADY_EXISTS = 10159; // tone_id_already_exists
    int VOICE_CLONE_HUOSHAN_VOICE_ID_ERROR = 10160; // volcano_engine_sound_id_format_error
}
