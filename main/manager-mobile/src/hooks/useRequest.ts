import type { Ref } from 'vue'

interface IUseRequestOptions<T> {
  /** whether_to_execute_immediately */
  immediate?: boolean
  /** initialization_data */
  initialData?: T
}

interface IUseRequestReturn<T> {
  loading: Ref<boolean>
  error: Ref<boolean | Error>
  data: Ref<T | undefined>
  run: () => Promise<T | undefined>
}

/*
*
* useRequest is a customized request hook, for_handling_asynchronous_requests_and_responses.
 * @param func a_function_that_performs_asynchronous_requests，returns_a_promise_containing_response_data。
 * @param options an_object_containing_request_options {immediate, initialData}。
 * @param options.immediate whether_to_execute_the_request_immediately，default_is_false。
 * @param options.initialData initialization_data，default_is_undefined。
 * @returns return_an_object{loading, error, data, run}，contains_the_loading_status_of_the_request、error_message、functions_to_respond_to_data_and_manually_trigger_requests。
*/
export default function useRequest<T>(
  func: () => Promise<IResData<T>>,
  options: IUseRequestOptions<T> = { immediate: false },
): IUseRequestReturn<T> {
  const loading = ref(false)
  const error = ref(false)
  const data = ref<T | undefined>(options.initialData) as Ref<T | undefined>
  const run = async () => {
    loading.value = true
    return func()
      .then((res) => {
        data.value = res.data
        error.value = false
        return data.value
      })
      .catch((err) => {
        error.value = err
        throw err
      })
      .finally(() => {
        loading.value = false
      })
  }

  options.immediate && run()
  return { loading, error, data, run }
}
