package xiaozhi.common.utils;

import lombok.extern.slf4j.Slf4j;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;

/**
 * hash_encryption_algorithm_tool_class
 * @author zjy
 */
@Slf4j
public class HashEncryptionUtil {
    /**
     * encrypt_using_md5
     * @param context encrypted_content
     * @return hash_value
     */
    public static String Md5hexDigest(String context){
        return hexDigest(context,"MD5");
    }

    /**
     * specify_hash_algorithm_for_encryption
     * @param context encrypted_content
     * @param algorithm hash_algorithm
     * @return hash_value
     */
   public static String hexDigest(String context,String algorithm ){
       // get_md5_algorithm_example
       MessageDigest md = null;
       try {
           md = MessageDigest.getInstance(algorithm);
       } catch (NoSuchAlgorithmException e) {
           log.error("Algorithm for encryption failure: {}",algorithm);
           throw new RuntimeException("Encryption failed,"+ algorithm +"Hash algorithm system does not support");
       }
       // calculate_the_md5_value_of_the_agent_id
       byte[] messageDigest = md.digest(context.getBytes());
       // convert_byte_array_to_hex_string
       StringBuilder hexString = new StringBuilder();
       for (byte b : messageDigest) {
           String hex = Integer.toHexString(0xFF & b);
           if (hex.length() == 1) {
               hexString.append('0');
           }
           hexString.append(hex);
       }
       return hexString.toString();
   }

}
