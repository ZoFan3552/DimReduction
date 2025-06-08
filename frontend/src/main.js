import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';

Vue.config.productionTip = false
Vue.use(ElementUI);

// // main.js
// window.addEventListener('error', e => {
//   if (e.message.includes('ResizeObserver')) e.stopImmediatePropagation()
// });

// // 也可用 window.onerror 拦截
// window.onerror = function (message) {
//   if (typeof message === 'string' && message.includes('ResizeObserver loop completed')) {
//     return true; // 返回 true 表示阻止默认行为
//   }
// };

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')
