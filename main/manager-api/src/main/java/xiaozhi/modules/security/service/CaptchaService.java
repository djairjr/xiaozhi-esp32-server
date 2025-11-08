package xiaozhi.modules.security.service;

import java.io.IOException;

import jakarta.servlet.http.HttpServletResponse;

/**
 * verification_code
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
public interface CaptchaService {

    /**
     * image_verification_code
     */
    void create(HttpServletResponse response, String uuid) throws IOException;

    /**
     * verification_code_validation
     * 
     * @param uuid   uuid
     * @param code   verification_code
     * @param delete whether_to_delete_the_verification_code
     * @return true：success false：fail
     */
    boolean validate(String uuid, String code, Boolean delete);

    /**
     * send_sms_verification_code
     * 
     * @param phone cell_phone
     */
    void sendSMSValidateCode(String phone);

    /**
     * verify_sms_verification_code
     * 
     * @param phone  cell_phone
     * @param code   verification_code
     * @param delete whether_to_delete_the_verification_code
     * @return true：success false：fail
     */
    boolean validateSMSValidateCode(String phone, String code, Boolean delete);
}
