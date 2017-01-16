// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import auth from './auth'
import App from './App'
import VueRouter from 'vue-router'
import HomePage from './components/HomePage/index.vue'
import AboutPage from './components/AboutPage/index.vue'
import AddComponentByTitle from './components/AddComponentByTitle/index.vue'
import AddFileFlowsToOrder from './components/AddFileFlowsToOrder/index.vue'
import AddOutputFilesToOrder from './components/AddOutputFilesToOrder/index.vue'
import AddTitleFromIMDb from './components/AddTitleFromIMDb/index.vue'
import AddTitleManually from './components/AddTitleManually/index.vue'
import ComponentsInOrder from './components/ComponentsInOrder/index.vue'
import DepartmentRequestDetail from './components/DepartmentRequestDetail/index.vue'
import DepartmentRequestLinks from './components/DepartmentRequestLinks/index.vue'
import DepartmentRequestTable from './components/DepartmentRequestTable/index.vue'
import LoginForm from './components/LoginForm/index.vue'
import OrderDetail from './components/OrderDetail/index.vue'
import OrderEntryForm from './components/OrderEntryForm/index.vue'
import OrderList from './components/OrderList/index.vue'
import SelectPipelines from './components/SelectPipelines/index.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: HomePage },
  { path: '/about', component: AboutPage },
  { path: '/department-requests/links', component: DepartmentRequestLinks, beforeEnter: requireAuth },
  { path: '/department-requests', component: DepartmentRequestTable, beforeEnter: requireAuth },
  { path: '/department-requests/:department', component: DepartmentRequestTable, beforeEnter: requireAuth },
  { path: '/department-requests/user', component: DepartmentRequestTable, beforeEnter: requireAuth },
  { path: '/department-request/:code', component: DepartmentRequestDetail, beforeEnter: requireAuth },
  { path: '/order_entry', component: OrderEntryForm, beforeEnter: requireAuth },
  { path: '/orders', component: OrderList, beforeEnter: requireAuth },
  { path: '/orders/:code', component: OrderDetail, beforeEnter: requireAuth },
  { path: '/orders/:code/file-flows/add', component: AddFileFlowsToOrder, beforeEnter: requireAuth },
  { path: '/orders/:code/titles/add', component: AddComponentByTitle, beforeEnter: requireAuth },
  { path: '/orders/:code/components', component: ComponentsInOrder, beforeEnter: requireAuth },
  { path: '/orders/:code/components/pipelines', component: SelectPipelines, beforeEnter: requireAuth },
  { path: '/orders/:code/output-files/add', component: AddOutputFilesToOrder, beforeEnter: requireAuth },
  { path: '/titles/add/imdb', component: AddTitleFromIMDb, beforeEnter: requireAuth },
  { path: '/titles/add/manual', component: AddTitleManually, beforeEnter: requireAuth },
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
