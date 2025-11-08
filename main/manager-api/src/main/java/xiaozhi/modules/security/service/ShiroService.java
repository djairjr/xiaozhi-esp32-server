package xiaozhi.modules.security.service;

import xiaozhi.modules.security.entity.SysUserTokenEntity;
import xiaozhi.modules.sys.entity.SysUserEntity;

/*
*
* Shiro related interfaces
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
*/
public interface ShiroService {

    SysUserTokenEntity getByToken(String token);

    /**
     * according_to_user_id，query_user
     *
     * @param userId
     */
    SysUserEntity getUser(Long userId);

}
