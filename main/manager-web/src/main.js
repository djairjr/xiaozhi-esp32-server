import 'element-ui/lib/theme-chalk/index.css';
import 'normalize.css/normalize.css'; // A modern alternative to CSS resets
import Vue from 'vue';
import ElementUI from 'element-ui';
import App from './App.vue';
import router from './router';
import store from './store';
import i18n from './i18n';
import './styles/global.scss';
import { register as registerServiceWorker } from './registerServiceWorker';

// create_event_bus，for_communication_between_components
Vue.prototype.$eventBus = new Vue();

Vue.use(ElementUI);

Vue.config.productionTip = false

// register_service Worker
registerServiceWorker();

// create_a_vue_instance
new Vue({
  router,
  store,
  i18n,
  render: function (h) { return h(App) }
}).$mount('#app')
