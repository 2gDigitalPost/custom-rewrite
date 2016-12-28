// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import auth from './auth'
import App from './App'
import VueRouter from 'vue-router'
import LoginForm from './components/LoginForm/index.vue'
import OrderEntryForm from './components/OrderEntryForm/index.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/order_entry', component: OrderEntryForm, beforeEnter: requireAuth },
  { path: '/login', component: LoginForm },
  { path: '/logout',
    beforeEnter (to, from, next) {
      auth.logout()
      next('/')
    }
  }
]

const router = new VueRouter({
  routes: routes
})

function requireAuth (to, from, next) {
  if (!auth.loggedIn()) {
    next({
      path: '/login',
      query: { redirect: to.fullPath }
    })
  } else {
    next()
  }
}

/* eslint-disable no-new */
new Vue({
  router,
  el: '#app',
  template: '<App/>',
  components: { App }
})
