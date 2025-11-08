/*
*
* cache_viewing_tool - used_to_check_whether_cdn_resources_have_been_serviced Worker cache
*/

/*
*
* get_all_services Worker cache name
 * @returns {Promise<string[]>} cache_name_list
*/
export const getCacheNames = async () => {
  if (!('caches' in window)) {
    return [];
  }
  
  try {
    return await caches.keys();
  } catch (error) {
    console.error('获取缓存名称失败:', error);
    return [];
  }
};

/**
 * get_all_urls_in_the_specified_cache
 * @param {string} cacheName cache_name
 * @returns {Promise<string[]>} cached_url_list
 */
export const getCacheUrls = async (cacheName) => {
  if (!('caches' in window)) {
    return [];
  }
  
  try {
    const cache = await caches.open(cacheName);
    const requests = await cache.keys();
    return requests.map(request => request.url);
  } catch (error) {
    console.error(`get_cache ${cacheName} url_failed:`, error);
    return [];
  }
};

/**
 * check_if_a_specific_url_has_been_cached
 * @param {string} url url_to_check
 * @returns {Promise<boolean>} is_it_cached
 */
export const isUrlCached = async (url) => {
  if (!('caches' in window)) {
    return false;
  }
  
  try {
    const cacheNames = await getCacheNames();
    for (const cacheName of cacheNames) {
      const cache = await caches.open(cacheName);
      const match = await cache.match(url);
      if (match) {
        return true;
      }
    }
    return false;
  } catch (error) {
    console.error(`check_url ${url} whether_cache_failed:`, error);
    return false;
  }
};

/**
 * get_the_cache_status_of_all_cdn_resources_on_the_current_page
 * @returns {Promise<Object>} cache_state_object
 */
export const checkCdnCacheStatus = async () => {
  // find_resources_from_cdn_cache
  const cdnCaches = ['cdn-stylesheets', 'cdn-scripts'];
  const results = {
    css: [],
    js: [],
    totalCached: 0,
    totalNotCached: 0
  };
  
  for (const cacheName of cdnCaches) {
    try {
      const urls = await getCacheUrls(cacheName);
      
      // differentiate_css_and_js_resources
      for (const url of urls) {
        if (url.endsWith('.css')) {
          results.css.push({ url, cached: true });
        } else if (url.endsWith('.js')) {
          results.js.push({ url, cached: true });
        }
        results.totalCached++;
      }
    } catch (error) {
      console.error(`get ${cacheName} caching_information_failed:`, error);
    }
  }
  
  return results;
};

/*
*
* clear_all_services Worker cache
 * @returns {Promise<boolean>} is_clearing_successful
*/
export const clearAllCaches = async () => {
  if (!('caches' in window)) {
    return false;
  }
  
  try {
    const cacheNames = await getCacheNames();
    for (const cacheName of cacheNames) {
      await caches.delete(cacheName);
    }
    return true;
  } catch (error) {
    console.error('清除所有缓存失败:', error);
    return false;
  }
};

/**
 * output_cache_status_to_console
 */
export const logCacheStatus = async () => {
  console.group('Service Worker 缓存状态');
  
  const cacheNames = await getCacheNames();
  console.log('已发现的缓存:', cacheNames);
  
  for (const cacheName of cacheNames) {
    const urls = await getCacheUrls(cacheName);
    console.group(`cache: ${cacheName} (${urls.length} item)`);
    urls.forEach(url => console.log(url));
    console.groupEnd();
  }
  
  console.groupEnd();
  return cacheNames.length > 0;
}; 