/* global self, workbox */

// Custom_service Worker installation and activation processing logic
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// CDN resource list
const CDN_CSS = [
  'https://unpkg.com/element-ui@2.15.14/lib/theme-chalk/index.css',
  'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css'
];

const CDN_JS = [
  'https://unpkg.com/vue@2.6.14/dist/vue.min.js',
  'https://unpkg.com/vue-router@3.6.5/dist/vue-router.min.js',
  'https://unpkg.com/vuex@3.6.2/dist/vuex.min.js',
  'https://unpkg.com/element-ui@2.15.14/lib/index.js',
  'https://unpkg.com/axios@0.27.2/dist/axios.min.js',
  'https://unpkg.com/opus-decoder@0.7.7/dist/opus-decoder.min.js'
];

// when_service Worker will be automatically executed after being injected into the manifest
const manifest = self.__WB_MANIFEST || [];

// check_if_cdn_mode_is_enabled
const isCDNEnabled = manifest.some(entry => 
  entry.url === 'cdn-mode' && entry.revision === 'enabled'
);

console.log(`Service Worker initialized, CDN模式: ${isCDNEnabled ? '启用' : '禁用'}`);

// inject_workbox_related_code
importScripts('https://storage.googleapis.com/workbox-cdn/releases/7.0.0/workbox-sw.js');
workbox.setConfig({ debug: false });

// open_workbox
workbox.core.skipWaiting();
workbox.core.clientsClaim();

// precaching_offline_pages
const OFFLINE_URL = '/offline.html';
workbox.precaching.precacheAndRoute([
  { url: OFFLINE_URL, revision: null }
]);

// add_installation_completion_event_handler，display_installation_messages_on_the_console
self.addEventListener('install', event => {
  if (isCDNEnabled) {
    console.log('Service Worker installed，开始缓存CDN资源');
  } else {
    console.log('Service Worker installed，CDN模式禁用，仅缓存本地资源');
  }
  
  // make_sure_offline_pages_are_cached
  event.waitUntil(
    caches.open('offline-cache').then((cache) => {
      return cache.add(OFFLINE_URL);
    })
  );
});

// add_activation_event_handler
self.addEventListener('activate', event => {
  console.log('Service Worker activated，现在控制着页面');
  
  // clean_old_version_cache
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.filter(cacheName => {
          // clear_cache_except_current_version
          return cacheName.startsWith('workbox-') && !workbox.core.cacheNames.runtime.includes(cacheName);
        }).map(cacheName => {
          return caches.delete(cacheName);
        })
      );
    })
  );
});

// add_fetch_event_interceptor，used_to_check_whether_cdn_resources_hit_the_cache
self.addEventListener('fetch', event => {
  // cdn_resource_cache_monitoring_is_only_performed_when_cdn_mode_is_enabled
  if (isCDNEnabled) {
    const url = new URL(event.request.url);
    
    // for_cdn_resources，output_information_about_whether_cache_is_hit
    if ([...CDN_CSS, ...CDN_JS].includes(url.href)) {
      // does_not_interfere_with_the_normal_fetch_process，just_add_logs
      console.log(`request_cdn_resources: ${url.href}`);
    }
  }
});

// only_cache_cdn_resources_in_cdn_mode
if (isCDNEnabled) {
  // caching_cdn_css_resources
  workbox.routing.registerRoute(
    ({ url }) => CDN_CSS.includes(url.href),
    new workbox.strategies.CacheFirst({
      cacheName: 'cdn-stylesheets',
      plugins: [
        new workbox.expiration.ExpirationPlugin({
          maxAgeSeconds: 365 * 24 * 60 * 60, // increase_cache_to_1_year
          maxEntries: 10, // cache_up_to_10_css_files
        }),
        new workbox.cacheableResponse.CacheableResponsePlugin({
          statuses: [0, 200], // caching_successful_responses
        }),
      ],
    })
  );

  // caching_cdns_js_resources
  workbox.routing.registerRoute(
    ({ url }) => CDN_JS.includes(url.href),
    new workbox.strategies.CacheFirst({
      cacheName: 'cdn-scripts',
      plugins: [
        new workbox.expiration.ExpirationPlugin({
          maxAgeSeconds: 365 * 24 * 60 * 60, // increase_cache_to_1_year
          maxEntries: 20, // cache_up_to_20_js_files
        }),
        new workbox.cacheableResponse.CacheableResponsePlugin({
          statuses: [0, 200], // caching_successful_responses
        }),
      ],
    })
  );
}

// whether_cdn_mode_is_enabled_or_not，all_cache_local_static_resources
workbox.routing.registerRoute(
  /\.(?:js|css|png|jpg|jpeg|svg|gif|ico|woff|woff2|eot|ttf|otf)$/,
  new workbox.strategies.StaleWhileRevalidate({
    cacheName: 'static-resources',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxAgeSeconds: 7 * 24 * 60 * 60, // 7 days cache
        maxEntries: 50, // cache_up_to_50_files
      }),
    ],
  })
);

// caching_html_pages
workbox.routing.registerRoute(
  /\.html$/,
  new workbox.strategies.NetworkFirst({
    cacheName: 'html-cache',
    plugins: [
      new workbox.expiration.ExpirationPlugin({
        maxAgeSeconds: 1 * 24 * 60 * 60, // 1 day cache
        maxEntries: 10, // cache_up_to_10_html_files
      }),
    ],
  })
);

// offline_page - use_more_reliable_processing
workbox.routing.setCatchHandler(async ({ event }) => {
  // returns_the_appropriate_default_page_based_on_the_request_type
  switch (event.request.destination) {
    case 'document':
      // if_it_is_a_web_request，return_to_offline_page
      return caches.match(OFFLINE_URL);
    default:
      // all_other_requests_return_an_error
      return Response.error();
  }
}); 