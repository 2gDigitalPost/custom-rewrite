/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import ProjectTemplateSelect from '../SelectWidgets/ProjectTemplateSelect'
import TaskStatusSelect from '../TaskStatusSelect/index.vue'

import bus from '../../bus'

export default {
  name: 'ProjectTemplateRequestDetail',
  components: {
    Multiselect,
    ProjectTemplateSelect,
    TaskStatusSelect
  },
  data () {
    return {
      loading: true,
      projectTemplateRequestObject: null,
      editingTaskStatus: false,
      statusComplete: false,
      selectedProjectTemplate: null
    }
  },
  methods: {
    loadProjectTemplateRequest: function () {
      let self = this
      self.loading = true
      self.editingTaskStatus = false
      self.statusComplete = false
      self.selectedProjectTemplate = null

      let codeParam = self.$route.params.code

      self.projectTemplateRequestObject = null

      axios.get('/api/v1/project-templates/requests/' + codeParam, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.projectTemplateRequestObject = response.data.project_template_request
        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    statusChanged: function (status) {
      if (status.toLowerCase() === 'complete') {
        this.statusComplete = true
      }
    },
    projectTemplateChange: function (projectTemplate) {
      this.selectedProjectTemplate = projectTemplate
    },
    editTaskStatusCancelled: function () {
      this.editingTaskStatus = false
    },
    getFileLink: function (fileName) {
      return 'http://localhost:8081/assets/project_template_request/' + this.projectTemplateRequestObject.code + '/' + fileName
    }
  },
  beforeMount: function () {
    this.loadProjectTemplateRequest()
  },
  created: function () {
    bus.$on('task-status-edit-cancel', this.editTaskStatusCancelled)
    bus.$on('selected-status-change', this.statusChanged)
    bus.$on('selected-project-template-change', this.projectTemplateChange)
    bus.$on('reload-page', this.loadProjectTemplateRequest)
  },
  destroyed: function () {
    bus.$off('task-status-edit-cancel', this.editTaskStatusCancelled)
    bus.$off('selected-status-change', this.statusChanged)
    bus.$off('selected-project-template-change', this.projectTemplateChange)
    bus.$off('reload-page', this.loadProjectTemplateRequest)
  },
}