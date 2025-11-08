package xiaozhi.modules.sys.dao;

import org.apache.ibatis.annotations.Mapper;

import xiaozhi.common.dao.BaseDao;
import xiaozhi.modules.sys.entity.SysUserEntity;

/**
 * system_user
 */
@Mapper
public interface SysUserDao extends BaseDao<SysUserEntity> {

}