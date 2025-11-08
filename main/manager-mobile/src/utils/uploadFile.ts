import { getEnvBaseUrl } from './index'
import { toast } from './toast'

/*
*
 * file_upload_hook_function_usage_example
 * @example
 * const { loading, error, data, progress, run } = useUpload<IUploadResult>(
 *   uploadUrl,
 *   {},
 *   {
 *     maxSize: 5, // maximum_5mb
 *     sourceType: ['album'], // only_supports_selection_from_albums
 *     onProgress: (p) => console.log(`upload_progress：${p}%`),
* onSuccess: (res) => console.log('Upload successful', res),
* onError: (err) => console.error('Upload failed', err),
 *   },
 * )
*/

/**
 * url_configuration_for_uploading_files
 */
export const uploadFileUrl = {
  /** user_avatar_upload_address（dynamically_read_the_current_effective BaseURL） */
  get USER_AVATAR() {
    return `${getEnvBaseUrl()}/user/avatar`
  },
}

/**
 * universal_file_upload_function（supports_directly_passing_in_file_path）
 * @param url upload_address
 * @param filePath local_file_path
 * @param formData additional_form_data
 * @param options upload_options
 */
export function useFileUpload<T = string>(url: string, filePath: string, formData: Record<string, any> = {}, options: Omit<UploadOptions, 'sourceType' | 'sizeType' | 'count'> = {}) {
  return useUpload<T>(
    url,
    formData,
    {
      ...options,
      sourceType: ['album'],
      sizeType: ['original'],
    },
    filePath,
  )
}

export interface UploadOptions {
  /** maximum_number_of_images_that_can_be_selected，default_is_1 */
  count?: number
  /** the_size_of_the_selected_image，original-original_picture，compressed-compressed_image */
  sizeType?: Array<'original' | 'compressed'>
  /** select_image_source，album-photo_album，camera-camera */
  sourceType?: Array<'album' | 'camera'>
  /** file_size_limit，unit：MB */
  maxSize?: number //
  /** upload_progress_callback_function */
  onProgress?: (progress: number) => void
  /** upload_success_callback_function */
  onSuccess?: (res: Record<string, any>) => void
  /** upload_failure_callback_function */
  onError?: (err: Error | UniApp.GeneralCallbackResult) => void
  /** upload_completion_callback_function（regardless_of_success_or_failure） */
  onComplete?: () => void
}

/**
 * file_upload_hook_function
 * @template T data_type_returned_after_successful_upload
 * @param url upload_address
 * @param formData additional_form_data
 * @param options upload_options
 * @returns upload_status_and_control_objects
 */
export function useUpload<T = string>(url: string, formData: Record<string, any> = {}, options: UploadOptions = {},
  /** directly_pass_in_the_file_path，skip_selector */
  directFilePath?: string) {
  /** uploading_status */
  const loading = ref(false)
  /** upload_error_status */
  const error = ref(false)
  /** response_data_after_successful_upload */
  const data = ref<T>()
  /** upload_progress（0-100） */
  const progress = ref(0)

  /** deconstructing_upload_options，set_default_value */
  const {
    /** maximum_number_of_images_that_can_be_selected */
    count = 1,
    /** the_size_of_the_selected_image */
    sizeType = ['original', 'compressed'],
    /** select_image_source */
    sourceType = ['album', 'camera'],
    /** file_size_limit（MB） */
    maxSize = 10,
    /** progress_callback */
    onProgress,
    /** successful_callback */
    onSuccess,
    /** failure_callback */
    onError,
    /** completion_callback */
    onComplete,
  } = options

  /**
   * check_if_file_size_exceeds_limit
   * @param size file_size（byte）
   * @returns passed_the_inspection
   */
  const checkFileSize = (size: number) => {
    const sizeInMB = size / 1024 / 1024
    if (sizeInMB > maxSize) {
      toast.warning(`file_size_cannot_exceed${maxSize}MB`)
      return false
    }
    return true
  }
  /**
   * trigger_file_selection_and_upload
   * use_different_selectors_depending_on_the_platform：
   * - using_wechat_mini_program chooseMedia
   * - use_on_other_platforms chooseImage
   */
  const run = () => {
    if (directFilePath) {
      // use_the_passed_file_path_directly
      loading.value = true
      progress.value = 0
      uploadFile<T>({
        url,
        tempFilePath: directFilePath,
        formData,
        data,
        error,
        loading,
        progress,
        onProgress,
        onSuccess,
        onError,
        onComplete,
      })
      return
    }

    // #ifdef MP-WEIXIN
    // used_in_wechat_mini_program_environment chooseMedia API
    uni.chooseMedia({
      count,
      mediaType: ['image'], // only_supports_image_types
      sourceType,
      success: (res) => {
        const file = res.tempFiles[0]
        // check_if_the_file_size_meets_the_limit
        if (!checkFileSize(file.size))
          return

        // start_uploading
        loading.value = true
        progress.value = 0
        uploadFile<T>({
          url,
          tempFilePath: file.tempFilePath,
          formData,
          data,
          error,
          loading,
          progress,
          onProgress,
          onSuccess,
          onError,
          onComplete,
        })
      },
      fail: (err) => {
        console.error('选择媒体文件失败:', err)
        error.value = true
        onError?.(err)
      },
    })
    // #endif

    // #ifndef MP-WEIXIN
    // used_in_nonwechat_mini_program_environment chooseImage API
    uni.chooseImage({
      count,
      sizeType,
      sourceType,
      success: (res) => {
        console.log('选择图片成功:', res)

        // start_uploading
        loading.value = true
        progress.value = 0
        uploadFile<T>({
          url,
          tempFilePath: res.tempFilePaths[0],
          formData,
          data,
          error,
          loading,
          progress,
          onProgress,
          onSuccess,
          onError,
          onComplete,
        })
      },
      fail: (err) => {
        console.error('选择图片失败:', err)
        error.value = true
        onError?.(err)
      },
    })
    // #endif
  }

  return { loading, error, data, progress, run }
}

/**
 * file_upload_options_interface
 * @template T data_type_returned_after_successful_upload
 */
interface UploadFileOptions<T> {
  /** upload_address */
  url: string
  /** temporary_file_path */
  tempFilePath: string
  /** additional_form_data */
  formData: Record<string, any>
  /** response_data_after_successful_upload */
  data: Ref<T | undefined>
  /** upload_error_status */
  error: Ref<boolean>
  /** uploading_status */
  loading: Ref<boolean>
  /** upload_progress（0-100） */
  progress: Ref<number>
  /** upload_progress_callback */
  onProgress?: (progress: number) => void
  /** upload_success_callback */
  onSuccess?: (res: Record<string, any>) => void
  /** upload_failure_callback */
  onError?: (err: Error | UniApp.GeneralCallbackResult) => void
  /** upload_complete_callback */
  onComplete?: () => void
}

/**
 * perform_file_upload
 * @template T data_type_returned_after_successful_upload
 * @param options upload_options
 */
function uploadFile<T>({
  url,
  tempFilePath,
  formData,
  data,
  error,
  loading,
  progress,
  onProgress,
  onSuccess,
  onError,
  onComplete,
}: UploadFileOptions<T>) {
  try {
    // create_upload_task
    const uploadTask = uni.uploadFile({
      url,
      filePath: tempFilePath,
      name: 'file', // file_corresponding_to key
      formData,
      header: {
        // In H5 environment, there is no need to manually set Content-Type, let_the_browser_automatically_handle_multipart_formats
        // #ifndef H5
        'Content-Type': 'multipart/form-data',
        // #endif
      },
      // make_sure_the_file_name_is_legal
      success: (uploadFileRes) => {
        console.log('上传文件成功:', uploadFileRes)
        try {
          // parse_response_data
          const { data: _data } = JSON.parse(uploadFileRes.data)
          // upload_successful
          data.value = _data as T
          onSuccess?.(_data)
        }
        catch (err) {
          // response_parsing_error
          console.error('解析上传响应失败:', err)
          error.value = true
          onError?.(new Error('上传响应解析失败'))
        }
      },
      fail: (err) => {
        // upload_request_failed
        console.error('上传文件失败:', err)
        error.value = true
        onError?.(err)
      },
      complete: () => {
        // execute_regardless_of_success_or_failure
        loading.value = false
        onComplete?.()
      },
    })

    // monitor_upload_progress
    uploadTask.onProgressUpdate((res) => {
      progress.value = res.progress
      onProgress?.(res.progress)
    })
  }
  catch (err) {
    // failed_to_create_upload_task
    console.error('创建上传任务失败:', err)
    error.value = true
    loading.value = false
    onError?.(new Error('创建上传任务失败'))
  }
}
