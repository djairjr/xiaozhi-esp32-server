// common_response_format
export interface IResponse<T = any> {
  code: number | string
  data: T
  msg: string
  status: string | number
}

// pagination_request_parameters
export interface PageParams {
  page: number
  pageSize: number
  [key: string]: any
}

// paginated_response_data
export interface PageResult<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
}
