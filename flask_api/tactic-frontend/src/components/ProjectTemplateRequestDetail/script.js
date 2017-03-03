/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

import EditTaskStatus from '../TaskDetail/EditTaskStatus/index.vue'

import bus from '../../bus'

export default {
  name: 'ProjectTemplateRequestDetail',
  components: {
    EditTaskStatus
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
  },
  beforeMount: function () {
    this.loadProjectTemplateRequest()
  }
}