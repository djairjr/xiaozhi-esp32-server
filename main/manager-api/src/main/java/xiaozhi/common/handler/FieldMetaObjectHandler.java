package xiaozhi.common.handler;

import java.util.Date;

import org.apache.ibatis.reflection.MetaObject;
import org.springframework.stereotype.Component;

import com.baomidou.mybatisplus.core.handlers.MetaObjectHandler;

import xiaozhi.common.constant.Constant;
import xiaozhi.common.user.UserDetail;
import xiaozhi.modules.security.user.SecurityUser;

/**
 * public_fields，autofill_value
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
@Component
public class FieldMetaObjectHandler implements MetaObjectHandler {
    private final static String CREATE_DATE = "createDate";
    private final static String CREATOR = "creator";
    private final static String UPDATE_DATE = "updateDate";
    private final static String UPDATER = "updater";

    private final static String DATA_OPERATION = "dataOperation";

    @Override
    public void insertFill(MetaObject metaObject) {
        UserDetail user = SecurityUser.getUser();
        Date date = new Date();

        // creator
        strictInsertFill(metaObject, CREATOR, Long.class, user.getId());
        // creation_time
        strictInsertFill(metaObject, CREATE_DATE, Date.class, date);

        // updater
        strictInsertFill(metaObject, UPDATER, Long.class, user.getId());
        // update_time
        strictInsertFill(metaObject, UPDATE_DATE, Date.class, date);

        // data_identification
        strictInsertFill(metaObject, DATA_OPERATION, String.class, Constant.DataOperation.INSERT.getValue());
    }

    @Override
    public void updateFill(MetaObject metaObject) {
        // updater
        strictUpdateFill(metaObject, UPDATER, Long.class, SecurityUser.getUserId());
        // update_time
        strictUpdateFill(metaObject, UPDATE_DATE, Date.class, new Date());

        // data_identification
        strictInsertFill(metaObject, DATA_OPERATION, String.class, Constant.DataOperation.UPDATE.getValue());
    }
}