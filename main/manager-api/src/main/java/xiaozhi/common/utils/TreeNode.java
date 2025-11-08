package xiaozhi.common.utils;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import lombok.Data;

/**
 * tree_node，all_that_need_to_be_implemented_to_implement_tree_nodes，all_need_to_inherit_this_class
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
@Data
public class TreeNode<T> implements Serializable {

    /**
     * primary_key
     */
    private Long id;
    /**
     * superior_id
     */
    private Long pid;
    /**
     * list_of_child_nodes
     */
    private List<T> children = new ArrayList<>();

}