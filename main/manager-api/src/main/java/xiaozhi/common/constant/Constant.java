package xiaozhi.common.constant;

import lombok.Getter;

/**
 * constant
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
public interface Constant {
    /**
     * success
     */
    int SUCCESS = 1;
    /**
     * fail
     */
    int FAIL = 0;
    /**
     * OK
     */
    String OK = "OK";
    /**
     * user_id
     */
    String USER_KEY = "userId";
    /**
     * menu_root_node_identifier
     */
    Long MENU_ROOT = 0L;
    /**
     * department_root_node_id
     */
    Long DEPT_ROOT = 0L;
    /**
     * data_dictionary_root_node_identifier
     */
    Long DICT_ROOT = 0L;
    /**
     * ascending_order
     */
    String ASC = "asc";
    /**
     * descending_order
     */
    String DESC = "desc";
    /**
     * creation_time_field_name
     */
    String CREATE_DATE = "create_date";

    /**
     * creation_time_field_name
     */
    String ID = "id";

    /**
     * data_permission_filtering
     */
    String SQL_FILTER = "sqlFilter";

    /**
     * current_page_number
     */
    String PAGE = "page";
    /**
     * display_number_of_records_per_page
     */
    String LIMIT = "limit";
    /**
     * sort_field
     */
    String ORDER_FIELD = "orderField";
    /**
     * sort_by
     */
    String ORDER = "order";

    /**
     * request_header_authorization_identifier
     */
    String AUTHORIZATION = "Authorization";

    /**
     * server_key
     */
    String SERVER_SECRET = "server.secret";

    /*
*
* SM2 public key
*/
    String SM2_PUBLIC_KEY = "server.public_key";

    /*
*
* SM2 private key
*/
    String SM2_PRIVATE_KEY = "server.private_key";

    /*
*
* websocket address
*/
    String SERVER_WEBSOCKET = "server.websocket";

    /**
     * mqtt gateway configuration
     */
    String SERVER_MQTT_GATEWAY = "server.mqtt_gateway";

    /*
*
*ota address
*/
    String SERVER_OTA = "server.ota";

    /**
     * whether_to_allow_user_registration
     */
    String SERVER_ALLOW_USER_REGISTER = "server.allow_user_register";

    /**
     * the_control_panel_address_displayed_when_issuing_a_sixdigit_verification_code
     */
    String SERVER_FRONTED_URL = "server.fronted_url";

    /**
     * path_separator
     */
    String FILE_EXTENSION_SEG = ".";

    /*
*
* mcp access point path
*/
    String SERVER_MCP_ENDPOINT = "server.mcp_endpoint";

    /*
*
* mcp access point path
*/
    String SERVER_VOICE_PRINT = "server.voice_print";

    /*
*
* mqtt key
*/
    String SERVER_MQTT_SECRET = "server.mqtt_signature_key";

    /**
     * no_memory
     */
    String MEMORY_NO_MEM = "Memory_nomem";

    /**
     * volcano_engine_binaural_voice_cloning
     */
    String VOICE_CLONE_HUOSHAN_DOUBLE_STREAM = "huoshan_double_stream";

    enum SysBaseParam {
        /*
*
* ICP registration number
*/
        BEIAN_ICP_NUM("server.beian_icp_num"),
        /*
*
*GA registration number
*/
        BEIAN_GA_NUM("server.beian_ga_num"),
        /**
         * system_name
         */
        SERVER_NAME("server.name");

        private String value;

        SysBaseParam(String value) {
            this.value = value;
        }

        public String getValue() {
            return value;
        }
    }

    /**
     * training_status
     */
    enum TrainStatus {
        /**
         * not_trained
         */
        NOT_TRAINED(0),
        /**
         * in_training
         */
        TRAINING(1),
        /**
         * trained
         */
        TRAINED(2),
        /**
         * training_failed
         */
        TRAIN_FAILED(3);

        private final int code;

        TrainStatus(int code) {
            this.code = code;
        }

        public int getCode() {
            return code;
        }
    }

    /**
     * system_sms
     */
    enum SysMSMParam {
        /**
         * alibaba_cloud_authorization_keyid
         */
        ALIYUN_SMS_ACCESS_KEY_ID("aliyun.sms.access_key_id"),
        /**
         * alibaba_cloud_authorization_key
         */
        ALIYUN_SMS_ACCESS_KEY_SECRET("aliyun.sms.access_key_secret"),
        /**
         * alibaba_cloud_sms_signature
         */
        ALIYUN_SMS_SIGN_NAME("aliyun.sms.sign_name"),
        /**
         * alibaba_cloud_sms_template
         */
        ALIYUN_SMS_SMS_CODE_TEMPLATE_CODE("aliyun.sms.sms_code_template_code"),
        /**
         * maximum_number_of_text_messages_sent_to_a_single_number
         */
        SERVER_SMS_MAX_SEND_COUNT("server.sms_max_send_count"),
        /**
         * whether_to_enable_mobile_phone_registration
         */
        SERVER_ENABLE_MOBILE_REGISTER("server.enable_mobile_register");

        private String value;

        SysMSMParam(String value) {
            this.value = value;
        }

        public String getValue() {
            return value;
        }
    }

    /**
     * data_status
     */
    enum DataOperation {
        /**
         * insert
         */
        INSERT("I"),
        /**
         * modified
         */
        UPDATE("U"),
        /**
         * deleted
         */
        DELETE("D");

        private String value;

        DataOperation(String value) {
            this.value = value;
        }

        public String getValue() {
            return value;
        }
    }

    @Getter
    enum ChatHistoryConfEnum {
        IGNORE(0, "Do not record"),
        RECORD_TEXT(1, "record text"),
        RECORD_TEXT_AUDIO(2, "Text and audio are recorded");

        private final int code;
        private final String name;

        ChatHistoryConfEnum(int code, String name) {
            this.code = code;
            this.name = name;
        }
    }

    /**
     * version_number
     */
    public static final String VERSION = "0.8.6";

    /**
     * invalid_firmware_url
     */
    String INVALID_FIRMWARE_URL = "http://xiaozhi.server.com:8002/xiaozhi/otaMag/download/NOT_ACTIVATED_FIRMWARE_THIS_IS_A_INVALID_URL";

    /**
     * dictionary_type
     */
    enum DictType {
        /**
         * mobile_phone_area_code
         */
        MOBILE_AREA("MOBILE_AREA");

        private String value;

        DictType(String value) {
            this.value = value;
        }

        public String getValue() {
            return value;
        }
    }
}