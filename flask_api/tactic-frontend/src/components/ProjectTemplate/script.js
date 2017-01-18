/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

export default {
  name: 'ProjectTemplate',
  components: {
    'multiselect': Multiselect
  },
  data () {
    return {
      templateCode: this.$route.params.code,
      componentTemplates: [],
      loading: true,
      template: null,
      newComponentTemplateFormVisible: false,
      newComponentName: null,
      newComponentSelectedPipeline: null,
      componentPipelineOptions: []
    }
  },
  methods: {
    loadProjectTemplate: function () {
      var self = this

      self.loading = true
      self.resetComponentTemplateForm()

      axios.get('/api/v1/project-templates/' + self.templateCode + '/full', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.template = response.data.project_template
        self.componentTemplates = response.data.component_templates

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadComponentPipelineOptions: function () {
      var self = this

      axios.get('/api/v1/pipelines/component', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.componentPipelineOptions = response.data.pipelines
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    toggleNewComponentTemplateForm: function () {
      let self = this

      self.newComponentTemplateFormVisible = !self.newComponentTemplateFormVisible
    },
    submitNewComponentTemplate: function () {
      let self = this

      let jsonToSend = {
        'name': self.newComponentName,
        'component_pipeline_code': self.newComponentSelectedPipeline.code,
        'project_template_code': self.templateCode,
        'token': localStorage.tactic_token
      }

      axios.post('/api/v1/component-templates', 
        JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            // Reload the page
            self.loadProjectTemplate()
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    resetComponentTemplateForm: function () {
      this.newComponentTemplateFormVisible = false
      this.newComponentSelectedPipeline = null
      this.newComponentName = null
    }
  },
  beforeMount: function () {
    this.loadProjectTemplate()
    this.loadComponentPipelineOptions()
  }
}