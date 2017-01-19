/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import AddFileFlowTemplateToComponentTemplateModal from './AddFileFlowTemplateToComponentTemplateModal/index.vue'

export default {
  name: 'ProjectTemplate',
  components: {
    'multiselect': Multiselect,
    'modal': AddFileFlowTemplateToComponentTemplateModal
  },
  data () {
    return {
      templateCode: this.$route.params.code,
      componentTemplates: [],
      packageTemplates: [],
      loading: true,
      template: null,
      newComponentTemplateFormVisible: false,
      newComponentName: null,
      newComponentSelectedPipeline: null,
      componentPipelineOptions: [],
      newPackageTemplateFormVisible: false,
      newPackageName: null,
      newPackageSelectedPipeline: null,
      packagePipelineOptions: [],
      newPackageSelectedPlatform: null,
      platformOptions: [],
      showModal: []
    }
  },
  methods: {
    loadProjectTemplate: function () {
      var self = this

      self.loading = true
      self.resetComponentTemplateForm()
      self.resetPackageTemplateForm()

      axios.get('/api/v1/project-templates/' + self.templateCode + '/full', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.template = response.data.project_template
        self.componentTemplates = response.data.component_templates
        self.packageTemplates = response.data.package_templates

        self.setupShowModalArray()

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
    loadPackagePipelineOptions: function () {
      var self = this

      axios.get('/api/v1/pipelines/package', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.packagePipelineOptions = response.data.pipelines
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadPlatformOptions: function () {
      var self = this

      axios.get('/api/v1/platforms', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.platformOptions = response.data.platforms
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    setupShowModalArray: function () {
      let self = this

      for (let i = 0; i < self.componentTemplates.length; i++) {
        self.showModal.push(false)
      }
    },
    toggleNewComponentTemplateForm: function () {
      this.newComponentTemplateFormVisible = !this.newComponentTemplateFormVisible
    },
    toggleNewPackageTemplateForm: function () {
      this.newPackageTemplateFormVisible = !this.newPackageTemplateFormVisible
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
    submitNewPackageTemplate: function () {
      let self = this

      let jsonToSend = {
        'name': self.newPackageName,
        'package_pipeline_code': self.newPackageSelectedPipeline.code,
        'platform_code': self.newPackageSelectedPlatform.code,
        'project_template_code': self.templateCode,
        'token': localStorage.tactic_token
      }

      axios.post('/api/v1/package-templates',
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
    },
    resetPackageTemplateForm: function () {
      this.newPackageTemplateFormVisible = false
      this.newPackageSelectedPipeline = null
      this.newPackageName = null
      this.newPackageSelectedPlatform = null
    }
  },
  beforeMount: function () {
    this.loadProjectTemplate()
    this.loadComponentPipelineOptions()
    this.loadPackagePipelineOptions()
    this.loadPlatformOptions()
  }
}