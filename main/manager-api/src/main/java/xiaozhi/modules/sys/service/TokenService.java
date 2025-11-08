package xiaozhi.modules.sys.service;

public interface TokenService {
    /**
     * generate_token
     *
     * @param userId
     * @return
     */
    String createToken(long userId);
}
