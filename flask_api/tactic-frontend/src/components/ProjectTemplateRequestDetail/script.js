/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import ProjectTemplateSelect from '../SelectWidgets/ProjectTemplateSelect'
import TaskStatusSelect from '../SelectWidgets/TaskStatusSelect/index.vue'

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
      editingProjectTemplate: false,
      selectedStatus: null,
      selectedProjectTemplate: null
    }
  },
  methods: {
    loadProjectTemplateRequest: function () {
      let self = this
      self.loading = true
      self.editingTaskStatus = false
      self.editingProjectTemplate = false
      self.selectedStatus = null
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
      this.selectedStatus = status
    },
    projectTemplateChange: function (projectTemplate) {
      this.selectedProjectTemplate = projectTemplate
    },
    editTaskStatusCancelled: function () {
      this.editingTaskStatus = false
    },
    getFileLink: function (fileName) {
      return 'http://localhost:8081/assets/project_template_request/' + this.projectTemplateRequestObject.code + '/' + fileName
    },
    submit: function () {
      let self = this

      let apiURL = '/api/v1/project-templates/requests/' + self.projectTemplateRequestObject.code

      let updateData = {}

      if (self.selectedStatus) {
        updateData['status'] = self.selectedStatus
      }
      if (self.selectedProjectTemplate) {
        updateData['project_template_code'] = self.selectedProjectTemplate.code
      }

      let jsonToSend = {
        'token': localStorage.tactic_token,
        'update_data': updateData
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('reload-page')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadProjectTemplateRequest()
  },
  computed: {
    showSubmit: function () {
      if (this.selectedStatus === null && this.selectedProjectTemplate === null) return false

      let currentStatus = this.projectTemplateRequestObject.task.status
      let currentProjectTemplate = this.projectTemplateRequestObject.project_template

      if (currentStatus !== this.selectedStatus) {
        if (this.selectedStatus && this.selectedStatus.toLowerCase() === 'complete') {
          return (!(currentProjectTemplate === null && this.selectedProjectTemplate === null))
        }
        else {
          return true
        }
      }
    }
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