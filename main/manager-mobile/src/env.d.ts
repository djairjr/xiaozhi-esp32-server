/// <reference types="vite/client" />
/// <reference types="vite-svg-loader" />

declare module '*.vue' {
  import type { DefineComponent } from 'vue'

  const component: DefineComponent<{}, {}, any>
  export default component
}

interface ImportMetaEnv {
  /** website_title，application_name */
  readonly VITE_APP_TITLE: string
  /** service_port_number */
  readonly VITE_SERVER_PORT: string
  /** backend_interface_address */
  readonly VITE_SERVER_BASEURL: string
  /* *Does H5 require an agent? */
  readonly VITE_APP_PROXY: 'true' | 'false'
  /* * Whether H5 requires a proxy, have_a_prefix_if_necessary */
  readonly VITE_APP_PROXY_PREFIX: string // usually/api
  /** upload_image_address */
  readonly VITE_UPLOAD_BASEURL: string
  /** whether_to_clear_the_console */
  readonly VITE_DELETE_CONSOLE: string
  // more_environment_variables...
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare const __VITE_APP_PROXY__: 'true' | 'false'
declare const __UNI_PLATFORM__: 'app' | 'h5' | 'mp-alipay' | 'mp-baidu' | 'mp-kuaishou' | 'mp-lark' | 'mp-qq' | 'mp-tiktok' | 'mp-weixin' | 'mp-xiaochengxu'
