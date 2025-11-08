package xiaozhi.modules.security.password;

/**
 * password_tools
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
public class PasswordUtils {
    private static PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    /**
     * encryption
     *
     * @param str string
     * @return return_encrypted_string
     */
    public static String encode(String str) {
        return passwordEncoder.encode(str);
    }

    /**
     * compare_passwords_for_equality
     *
     * @param str      clear_text_password
     * @param password encrypted_password
     * @return true：success false：fail
     */
    public static boolean matches(String str, String password) {
        return passwordEncoder.matches(str, password);
    }

    public static void main(String[] args) {
        String str = "admin";
        String password = encode(str);

        System.out.println(password);
        System.out.println(matches(str, password));
    }

}
