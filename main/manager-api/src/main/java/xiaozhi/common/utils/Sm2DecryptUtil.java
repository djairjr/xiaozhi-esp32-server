package xiaozhi.common.utils;

import org.apache.commons.lang3.StringUtils;
import xiaozhi.common.constant.Constant;
import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.exception.RenException;
import xiaozhi.modules.security.service.CaptchaService;
import xiaozhi.modules.sys.service.SysParamsService;

/*
*
* SM2 decryption and verification code verification tool class
 * encapsulated_duplicate_sm2_decryption、captcha_extraction_and_verification_logic
*/
public class Sm2DecryptUtil {
    
    /**
     * verification_code_length
     */
    private static final int CAPTCHA_LENGTH = 5;
    
    /*
*
     * decrypt_sm2_encrypted_content，extract_the_verification_code_and_verify
* @param encryptedPassword SM2 encrypted password string
     * @param captchaId verification_code_id
     * @param captchaService verification_code_service
     * @param sysParamsService system_parameter_service
     * @return the_actual_password_after_decryption
*/
    public static String decryptAndValidateCaptcha(String encryptedPassword, String captchaId, 
                                                 CaptchaService captchaService, SysParamsService sysParamsService) {
        // get_sm2_private_key
        String privateKeyStr = sysParamsService.getValue(Constant.SM2_PRIVATE_KEY, true);
        if (StringUtils.isBlank(privateKeyStr)) {
            throw new RenException(ErrorCode.SM2_KEY_NOT_CONFIGURED);
        }
        
        // decrypt_password_using_sm2_private_key
        String decryptedContent;
        try {
            decryptedContent = SM2Utils.decrypt(privateKeyStr, encryptedPassword);
        } catch (Exception e) {
            throw new RenException(ErrorCode.SM2_DECRYPT_ERROR);
        }
        
        // separate_verification_code_and_password：the_first_5_digits_are_verification_code，followed_by_password
        if (decryptedContent.length() > CAPTCHA_LENGTH) {
            String embeddedCaptcha = decryptedContent.substring(0, CAPTCHA_LENGTH);
            String actualPassword = decryptedContent.substring(CAPTCHA_LENGTH);
            
            // verify_that_the_embedded_verification_code_is_correct
            boolean embeddedCaptchaValid = captchaService.validate(captchaId, embeddedCaptcha, true);
            if (!embeddedCaptchaValid) {
                throw new RenException(ErrorCode.SMS_CAPTCHA_ERROR);
            }
            
            return actualPassword;
        } else {
            throw new RenException(ErrorCode.SM2_DECRYPT_ERROR);
        }
    }
}