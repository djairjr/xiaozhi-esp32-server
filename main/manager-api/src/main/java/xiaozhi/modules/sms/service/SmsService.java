package xiaozhi.modules.sms.service;

/**
 * sms_service_method_definition_interface
 *
 * @author zjy
 * @since 2025-05-12
 */
public interface SmsService {

    /**
     * send_verification_code_sms
     * @param phone phone_number
     * @param VerificationCode verification_code
     */
    void sendVerificationCodeSms(String phone, String VerificationCode) ;
}
