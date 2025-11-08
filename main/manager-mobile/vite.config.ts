import path from 'node:path'
import process from 'node:process'
import Uni from '@dcloudio/vite-plugin-uni'
import Components from '@uni-helper/vite-plugin-uni-components'
// @see https://uni-helper.js.org/vite-plugin-uni-layouts
import UniLayouts from '@uni-helper/vite-plugin-uni-layouts'
// @see https://github.com/uni-helper/vite-plugin-uni-manifest
import UniManifest from '@uni-helper/vite-plugin-uni-manifest'
// @see https://uni-helper.js.org/vite-plugin-uni-pages
import UniPages from '@uni-helper/vite-plugin-uni-pages'
// @see https://github.com/uni-helper/vite-plugin-uni-platform
// need_and @uni-helper/vite-plugin-uni-pages plugins_are_used_together_with
import UniPlatform from '@uni-helper/vite-plugin-uni-platform'
/**
 * subcontracting_optimization、module_asynchronous_crosspackage_call、component_asynchronous_crosspackage_reference
 * @see https://github.com/uni-ku/bundle-optimizer
 */
import Optimization from '@uni-ku/bundle-optimizer'
import dayjs from 'dayjs'
import { visualizer } from 'rollup-plugin-visualizer'
import AutoImport from 'unplugin-auto-import/vite'
import { defineConfig, loadEnv } from 'vite'
import ViteRestart from 'vite-plugin-restart'

// https://vitejs.dev/config/
export default async ({ command, mode }) => {
  // @see https://unocss.dev/
  const UnoCSS = (await import('unocss/vite')).default
  // console.log(mode === process.env.NODE_ENV) // true

  // mode: distinguish_between_production_environment_and_development_environment
  console.log('command, mode -> ', command, mode)
  // pnpm dev:h5 get_when => serve development
  // pnpm build:h5 get_when => build production
  // pnpm dev:mp-weixin get_when => build development (note_the_difference, command is build)
  // pnpm build:mp-weixin get_when => build production
  // pnpm dev:app get_when => build development (note_the_difference, command is build)
  // pnpm build:app get_when => build production
  // dev and build the_commands_can_be_used_separately .env.development and .env.production environment_variables

  const { UNI_PLATFORM } = process.env
  console.log('UNI_PLATFORM -> ', UNI_PLATFORM) // get mp-weixin, h5, app wait

  const env = loadEnv(mode, path.resolve(process.cwd(), 'env'))
  const {
    VITE_APP_PORT,
    VITE_SERVER_BASEURL,
    VITE_DELETE_CONSOLE,
    VITE_SHOW_SOURCEMAP,
    VITE_APP_PUBLIC_BASE,
    VITE_APP_PROXY,
    VITE_APP_PROXY_PREFIX,
  } = env
  console.log('环境变量 env -> ', env)

  return defineConfig({
    envDir: './env', // custom_env_directory
    base: VITE_APP_PUBLIC_BASE,
    plugins: [
      UniPages({
        exclude: ['**/components/**/**.*'],
        // HomePage pass vue documentary route-block type="home" to set
        // pages the_directory_is src/pages，the_subpackage_directory_cannot_be_configured_in_the_pages_directory
        subPackages: ['src/pages-sub'], // is_an_array，can_configure_multiple，but_it_cannot_be_the_directory_in_pages
        dts: 'src/types/uni-pages.d.ts',
      }),
      UniLayouts(),
      UniPlatform(),
      UniManifest(),
      // UniXXX need_to_be_in Uni introduced_before
      {
        // temporary_solution dcloudio official @dcloudio/uni-mp-compiler the_compilation_that_occurs BUG
        // refer_to github issue: https://github.com/dcloudio/uni-app/issues/4952
        // custom_plugin_disabled vite:vue plugin devToolsEnabled，force_compilation vue template inline for true
        name: 'fix-vite-plugin-vue',
        configResolved(config) {
          const plugin = config.plugins.find(p => p.name === 'vite:vue')
          if (plugin && plugin.api && plugin.api.options) {
            plugin.api.options.devToolsEnabled = false
          }
        },
      },
      UnoCSS(),
      AutoImport({
        imports: ['vue', 'uni-app'],
        dts: 'src/types/auto-import.d.ts',
        dirs: ['src/hooks'], // automatic_import hooks
        vueTemplate: true, // default false
      }),
      // Optimization plugin_requires page.json document，therefore_it_should_be UniPages execute_after_plugin
      Optimization({
        enable: {
          'optimization': true,
          'async-import': true,
          'async-component': true,
        },
        dts: {
          base: 'src/types',
        },
        logger: false,
      }),

      ViteRestart({
        // through_this_plugin, modifying_vite.config.js file does not need to be re-run for the configuration to take effect.
        restart: ['vite.config.js'],
      }),
      // h5 environment adds BUILD_TIME and BUILD_BRANCH
      UNI_PLATFORM === 'h5' && {
        name: 'html-transform',
        transformIndexHtml(html) {
          return html.replace('%BUILD_TIME%', dayjs().format('YYYY-MM-DD HH:mm:ss'))
        },
      },
      // packaged_analysis_plugin，h5 + the_production_environment_only_pops_up
      UNI_PLATFORM === 'h5'
      && mode === 'production'
      && visualizer({
        filename: './node_modules/.cache/visualizer/stats.html',
        open: true,
        gzipSize: true,
        brotliSize: true,
      }),
      // only_in app only_enabled_on_the_platform copyNativeRes plugin
      // UNI_PLATFORM === 'app' && copyNativeRes(),
      Components({
        extensions: ['vue'],
        deep: true, // whether_to_scan_subdirectories_recursively，
        directoryAsNamespace: false, // whether_to_use_the_directory_name_as_a_namespace_prefix，true when_the_component_name_is directory_name+component_name，
        dts: 'src/types/components.d.ts', // automatically_generated_component_type_declaration_file_path（used_for TypeScript support）
      }),
      Uni(),
    ],
    define: {
      __UNI_PLATFORM__: JSON.stringify(UNI_PLATFORM),
      __VITE_APP_PROXY__: JSON.stringify(VITE_APP_PROXY),
    },
    css: {
      postcss: {
        plugins: [
          // autoprefixer({
          //   // specify_target_browser
          //   overrideBrowserslist: ['> 1%', 'last 2 versions'],
          // }),
        ],
      },
    },

    resolve: {
      alias: {
        '@': path.join(process.cwd(), './src'),
        '@img': path.join(process.cwd(), './src/static/images'),
      },
    },
    server: {
      host: '0.0.0.0',
      hmr: true,
      port: Number.parseInt(VITE_APP_PORT, 10),
      // only H5 valid_on_the_terminal，does_not_take_effect_on_other_terminals（build_on_other_terminals，dont_leave_devserver)
      proxy: JSON.parse(VITE_APP_PROXY)
        ? {
            [VITE_APP_PROXY_PREFIX]: {
              target: VITE_SERVER_BASEURL,
              changeOrigin: true,
              rewrite: path => path.replace(new RegExp(`^${VITE_APP_PROXY_PREFIX}`), ''),
            },
          }
        : undefined,
    },
    esbuild: {
      drop: VITE_DELETE_CONSOLE === 'true' ? ['console', 'debugger'] : ['debugger'],
    },
    build: {
      sourcemap: false,
      // convenient_for_nonh5_end_debugging
      // sourcemap: VITE_SHOW_SOURCEMAP === 'true', // the_default_is_false
      target: 'es6',
      // no_need_to_compress_the_development_environment
      minify: mode === 'development' ? false : 'esbuild',

    },
  })
}
