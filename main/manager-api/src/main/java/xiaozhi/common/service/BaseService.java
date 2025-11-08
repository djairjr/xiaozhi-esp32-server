package xiaozhi.common.service;

import java.io.Serializable;
import java.util.Collection;

import com.baomidou.mybatisplus.core.conditions.Wrapper;

/**
 * basic_service_interface，all_service_interfaces_must_inherit
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
public interface BaseService<T> {
    Class<T> currentModelClass();

    /**
     * <p>
     * insert_a_record（select_field，policy_insertion）
     * </p>
     *
     * @param entity entity_object
     */
    boolean insert(T entity);

    /**
     * <p>
     * insert（batch），this_method_does_not_support Oracle、SQL Server
     * </p>
     *
     * @param entityList entity_object_collection
     */
    boolean insertBatch(Collection<T> entityList);

    /**
     * <p>
     * insert（batch），this_method_does_not_support Oracle、SQL Server
     * </p>
     *
     * @param entityList entity_object_collection
     * @param batchSize  insert_batch_quantity
     */
    boolean insertBatch(Collection<T> entityList, int batchSize);

    /**
     * <p>
     * according_to ID select_edit
     * </p>
     *
     * @param entity entity_object
     */
    boolean updateById(T entity);

    /**
     * <p>
     * according_to whereEntity condition，update_record
     * </p>
     *
     * @param entity        entity_object
     * @param updateWrapper entity_object_encapsulation_operation_class
     *                      {@link com.baomidou.mybatisplus.core.conditions.update.UpdateWrapper}
     */
    boolean update(T entity, Wrapper<T> updateWrapper);

    /**
     * <p>
     * according_to_id batch_update
     * </p>
     *
     * @param entityList entity_object_collection
     */
    boolean updateBatchById(Collection<T> entityList);

    /**
     * <p>
     * according_to_id batch_update
     * </p>
     *
     * @param entityList entity_object_collection
     * @param batchSize  update_batch_quantity
     */
    boolean updateBatchById(Collection<T> entityList, int batchSize);

    /**
     * <p>
     * according_to ID query
     * </p>
     *
     * @param id primary_key_id
     */
    T selectById(Serializable id);

    /**
     * <p>
     * according_to ID delete
     * </p>
     *
     * @param id primary_key_id
     */
    boolean deleteById(Serializable id);

    /**
     * <p>
     * delete（according_to_id batch_delete）
     * </p>
     *
     * @param idList primary_key_id_list
     */
    boolean deleteBatchIds(Collection<? extends Serializable> idList);
}