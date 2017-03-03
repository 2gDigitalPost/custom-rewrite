// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import auth from './auth'
import App from './App'
import VueRouter from 'vue-router'
import HomePage from './components/HomePage/index.vue'
import AddComponentByTitleFull from './components/AddComponentByTitleFull/index.vue'
import AddFileFlowsToOrder from './components/AddFileFlowsToOrder/index.vue'
import AddOutputFilesToOrder from './components/AddOutputFilesToOrder/index.vue'
import AddTitleFromIMDb from './components/AddTitleFromIMDb/index.vue'
import AddTitleManually from './components/AddTitleManually/index.vue'
import ClientDetail from './components/ClientDetail/index.vue'
import ClientTable from './components/ClientTable/index.vue'
import ComponentsInOrder from './components/ComponentsInOrder/index.vue'
import DepartmentRequestDetail from './components/DepartmentRequestDetail/index.vue'
import DepartmentRequestLinks from './components/DepartmentRequestLinks/index.vue'
import DepartmentRequestTable from './components/DepartmentRequestTable/index.vue'
import EditableInstructionsDocument from './components/EditableInstructionsDocument/index.vue'
import ElementEvaluationTable from './components/ElementEvaluationTable/index.vue'
import ImportTemplateToOrder from './components/ImportTemplateToOrder/index.vue'
import InstructionsTemplate from './components/InstructionsTemplate/index.vue'
import InstructionsTemplatesList from './components/InstructionsTemplatesList/index.vue'
import LoginForm from './components/LoginForm/index.vue'
import NewInstructionsTemplate from './components/NewInstructionsTemplate/index.vue'
import NewProjectTemplateForm from './components/NewProjectTemplateForm/index.vue'
import OrderDetail from './components/OrderDetail/index.vue'
import OrderEntryForm from './components/OrderEntryForm/index.vue'
import OrderList from './components/OrderList/index.vue'
import PlatformTable from './components/PlatformTable/index.vue'
import ProjectTemplate from './components/ProjectTemplate/index.vue'
import ProjectTemplatesList from './components/ProjectTemplatesList/index.vue'
import ProjectTemplateRequest from './components/ProjectTemplateRequest/index.vue'
import ProjectTemplateRequestDetail from './components/ProjectTemplateRequestDetail/index.vue'
import ProjectTemplateRequestTable from './components/ProjectTemplateRequestTable/index.vue'
import SelectPipelines from './components/SelectPipelines/index.vue'
import TaskDetail from './components/TaskDetail/index.vue'
import TaskLinks from './components/TaskLinks/index.vue'
import TaskTable from './components/TaskTable/index.vue'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: HomePage },
  { path: '/department-requests/links', component: DepartmentRequestLinks, beforeEnter: requireAuth },
  { path: '/department-requests', component: DepartmentRequestTable, beforeEnter: requireAuth },
  { path: '/department-requests/:department', component: DepartmentRequestTable, beforeEnter: requireAuth },
  { path: '/department-requests/user', component: DepartmentRequestTable, beforeEnter: requireAuth },
  { path: '/department-request/:code', component: DepartmentRequestDetail, beforeEnter: requireAuth },
  { path: '/orders', component: OrderList, beforeEnter: requireAuth },
  { path: '/orders/new', component: OrderEntryForm, beforeEnter: requireAuth },
  { path: '/orders/:code', component: OrderDetail, beforeEnter: requireAuth },
  { path: '/orders/:code/file-flows/add', component: AddFileFlowsToOrder, beforeEnter: requireAuth },
  { path: '/orders/:code/titles/add', component: AddComponentByTitleFull, beforeEnter: requireAuth },
  { path: '/orders/:code/components', component: ComponentsInOrder, beforeEnter: requireAuth },
  { path: '/orders/:code/components/pipelines', component: SelectPipelines, beforeEnter: requireAuth },
  { path: '/orders/:code/output-files/add', component: AddOutputFilesToOrder, beforeEnter: requireAuth },
  { path: '/orders/:code/template/add', component: ImportTemplateToOrder, beforeEnter: requireAuth },
  { path: '/titles/add/imdb', component: AddTitleFromIMDb, beforeEnter: requireAuth },
  { path: '/titles/add/manual', component: AddTitleManually, beforeEnter: requireAuth },
  { path: '/task/:code', component: TaskDetail, beforeEnter: requireAuth },
  { path: '/tasks/links', component: TaskLinks, beforeEnter: requireAuth },
  { path: '/tasks/user', component: TaskTable, beforeEnter: requireAuth },
  { path: '/tasks/:department', component: TaskTable, beforeEnter: requireAuth },
  { path: '/tasks', component: TaskTable, beforeEnter: requireAuth },
  { path: '/clients', component: ClientTable, beforeEnter: requireAuth },
  { path: '/clients/:code', component: ClientDetail, beforeEnter: requireAuth },
  { path: '/platforms', component: PlatformTable, beforEnter: requireAuth },
  { path: '/element-evaluations', component: ElementEvaluationTable, beforeEnter: requireAuth },
  { path: '/project-templates', component: ProjectTemplatesList, beforeEnter: requireAuth },
  { path: '/project-templates/request', component: ProjectTemplateRequest, beforeEnter: requireAuth },
  { path: '/project-templates/requests', component: ProjectTemplateRequestTable, beforeEnter: requireAuth },
  { path: '/project-templates/requests/:code', component: ProjectTemplateRequestDetail, beforeEnter: requireAuth },
  { path: '/project-templates/new', component: NewProjectTemplateForm, beforeEnter: requireAuth },
  { path: '/project-templates/:code', component: ProjectTemplate, beforeEnter: requireAuth },
  { path: '/instructions/:code', component: EditableInstructionsDocument, beforeEnter: requireAuth },
  { path: '/instructions-templates/', component: InstructionsTemplatesList, beforeEnter: requireAuth },
  { path: '/instructions-templates/new', component: NewInstructionsTemplate, beforeEnter: requireAuth },
  { path: '/instructions-templates/:code', component: InstructionsTemplate, beforeEnter: requireAuth },
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
