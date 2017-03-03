/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

import TaskStatusSelect from '../TaskStatusSelect/index.vue'

import bus from '../../bus'

export default {
  name: 'ProjectTemplateRequestDetail',
  components: {
    TaskStatusSelect
  },
  data () {
    return {
      loading: true,
      projectTemplateRequestObject: null,
      editingTaskStatus: false
    }
  },
  methods: {
    loadProjectTemplateRequest: function () {
      let self = this
      self.loading = true
      self.editingTaskStatus = false

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
    editTaskStatusCancelled: function () {
      this.editingTaskStatus = false
    }
  },
  beforeMount: function () {
    this.loadProjectTemplateRequest()
  },
  created: function () {
    bus.$on('task-status-edit-cancel', this.editTaskStatusCancelled)
    bus.$on('reload-page', this.loadProjectTemplateRequest)
  },
  destroyed: function () {
    bus.$off('task-status-edit-cancel', this.editTaskStatusCancelled)
    bus.$off('reload-page', this.loadProjectTemplateRequest)
  },
}