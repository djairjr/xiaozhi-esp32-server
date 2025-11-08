const { defineConfig } = require('@vue/cli-service');
const dotenv = require('dotenv');
// TerserPlugin for_compression JavaScript
const TerserPlugin = require('terser-webpack-plugin');
// CompressionPlugin turn_on Gzip compression
const CompressionPlugin = require('compression-webpack-plugin')
// BundleAnalyzerPlugin used_to_analyze_packaged_files
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
// WorkboxPlugin used_to_generate_service Worker
const { InjectManifest } = require('workbox-webpack-plugin');
// introduce path module

const path = require('path')
 
function resolve(dir) {
  return path.join(__dirname, dir)
}

// make_sure_to_load .env document
dotenv.config();

// define_cdn_resource_list, ensure_service Worker can also access
const cdnResources = {
  css: [
    'https://unpkg.com/element-ui@2.15.14/lib/theme-chalk/index.css',
    'https://cdnjs.cloudflare.com/ajax/libs/normalize/8.0.1/normalize.min.css'
  ],
  js: [
    'https://unpkg.com/vue@2.6.14/dist/vue.min.js',
    'https://unpkg.com/vue-router@3.6.5/dist/vue-router.min.js',
    'https://unpkg.com/vuex@3.6.2/dist/vuex.min.js',
    'https://unpkg.com/element-ui@2.15.14/lib/index.js',
    'https://unpkg.com/axios@0.27.2/dist/axios.min.js',
    'https://unpkg.com/opus-decoder@0.7.7/dist/opus-decoder.min.js'
  ]
};

// determine_whether_to_use_cdn
const useCDN = process.env.VUE_APP_USE_CDN === 'true';

module.exports = defineConfig({
  productionSourceMap: process.env.NODE_ENV !=='production', // the_production_environment_is_not_generated source map
  devServer: {
    port: 8001, // the_specified_port_is 8001
    proxy: {
      '/xiaozhi': {
        target: 'http://127.0.0.1:8002',
        changeOrigin: true
      }
    },
    client: {
      overlay: false, // dont_show webpack error_overlay
    },
  },
  publicPath: process.env.VUE_APP_PUBLIC_PATH || "/",
  chainWebpack: config => {

    // revise HTML plugin_configuration，dynamic_insertion CDN link
    config.plugin('html')
      .tap(args => {
        // decide_whether_to_use_cdn_based_on_configuration
        if (process.env.NODE_ENV === 'production' && useCDN) {
          args[0].cdn = cdnResources;
        }
        return args;
      });

    // code_splitting_optimization
    config.optimization.splitChunks({
      chunks: 'all',
      minSize: 20000,
      maxSize: 250000,
      cacheGroups: {
        vendors: {
          name: 'chunk-vendors',
          test: /[\\/]node_modules[\\/]/,
          priority: -10,
          chunks: 'initial',
        },
        common: {
          name: 'chunk-common',
          minChunks: 2,
          priority: -20,
          chunks: 'initial',
          reuseExistingChunk: true,
        },
      }
    });

    // enable_optimization_settings
    config.optimization.usedExports(true);
    config.optimization.concatenateModules(true);
    config.optimization.minimize(true);
  },
  configureWebpack: config => {
    if (process.env.NODE_ENV === 'production') {
      // enable_multithreaded_compilation
      config.optimization = {
        minimize: true,
        minimizer: [
          new TerserPlugin({
            parallel: true,
            terserOptions: {
              compress: {
                drop_console: true,
                drop_debugger: true,
                pure_funcs: ['console.log']
              }
            }
          })
        ]
      };
      config.plugins.push(
        new CompressionPlugin({
          algorithm: 'gzip',
          test: /\.(js|css|html|svg)$/,
          threshold: 20480,
          minRatio: 0.8
        })
      );

      // decide_whether_to_add_service_based_on_whether_to_use_cdn Worker
      config.plugins.push(
        new InjectManifest({
          swSrc: path.resolve(__dirname, 'src/service-worker.js'),
          swDest: 'service-worker.js',
          exclude: [/\.map$/, /asset-manifest\.json$/],
          maximumFileSizeToCacheInBytes: 5 * 1024 * 1024, // 5MB
          // custom_service Worker injection point
          injectionPoint: 'self.__WB_MANIFEST',
          // add_additional_information_to_pass_to_service Worker
          additionalManifestEntries: useCDN ?
            [{ url: 'cdn-mode', revision: 'enabled' }] :
            [{ url: 'cdn-mode', revision: 'disabled' }]
        })
      );

      // if_using_cdn，then_configure_externals_to_exclude_dependent_packages
      if (useCDN) {
        config.externals = {
          'vue': 'Vue',
          'vue-router': 'VueRouter',
          'vuex': 'Vuex',
          'element-ui': 'ELEMENT',
          'axios': 'axios',
          'opus-decoder': 'OpusDecoder'
        };
      } else {
        // make_sure_externals_is_not_set_when_not_using_a_cdn，let_webpack_package_all_dependencies
        config.externals = {};
      }

      if (process.env.ANALYZE === 'true') {  // controlled_by_environment_variables
        config.plugins.push(
          new BundleAnalyzerPlugin({
            analyzerMode: 'server',    // enable_local_server_mode
            openAnalyzer: true,        // automatically_open_browser
            analyzerPort: 8888         // specify_port_number
          })
        );
      }
      config.cache = {
        type: 'filesystem',  // use_file_system_caching
        cacheDirectory: path.resolve(__dirname, '.webpack_cache'),  // custom_cache_directory
        allowCollectingMemory: true,  // enable_memory_collection
        compression: 'gzip',  // enable_gzip_compression_caching
        maxAge: 5184000000, // the_cache_validity_period_is 1 month
        buildDependencies: {
          config: [__filename]  // the_cache_is_invalidated_every_time_the_configuration_file_is_modified
        }
      };
    }
  },
  // expose_cdn_resource_information_to_service-worker.js
  pwa: {
    workboxOptions: {
      skipWaiting: true,
      clientsClaim: true
    }
  }
});
