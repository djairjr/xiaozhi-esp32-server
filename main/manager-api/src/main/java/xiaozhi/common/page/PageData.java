package xiaozhi.common.page;

import java.io.Serializable;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * paging_tool_class
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
@Data
@Schema(description = "Paginated data")
public class PageData<T> implements Serializable {
    @Schema(description = "Total number of records")
    private int total;

    @Schema(description = "List data")
    private List<T> list;

    /**
     * pagination
     *
     * @param list  list_data
     * @param total total_number_of_records
     */
    public PageData(List<T> list, long total) {
        this.list = list;
        this.total = (int) total;
    }
}