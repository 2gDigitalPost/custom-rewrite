/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../../../bus'

export default {
  name: 'ComponentEntryForm',
  props: ['orderCode'],
  components: {
    'multiselect': Multiselect,
  },
  data () {
    return {
      loading: false,
      name: null,
      selectedPipeline: null,
      selectedTitle: null,
      selectedInstructionsTemplate: null,
      componentPipelineOptions: [],
      titleOptions: [],
      componentInstructionsTemplateOptions: [],
      errors: []
    }
  },
  methods: {
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
    loadTitleOptions: function () {
      let self = this

      axios.get('/api/v1/titles', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.titleOptions = response.data.titles
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadComponentInstructionsTemplateOptions: function () {
      let self = this

      axios.get('/api/v1/instructions-templates', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.componentInstructionsTemplateOptions = response.data.instructions_templates
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submit: function () {
      let self = this
      self.errors = []

      if (!self.name) {
        self.errors.push('name')
      }
      if (!self.selectedPipeline) {
        self.errors.push('pipeline')
      }

      if (self.errors.length > 0) {
        return
      }

      let jsonToSend = {
        'name': self.name,
        'order_code': self.orderCode,
        'pipeline_code': self.selectedPipeline.code,
        'token': localStorage.tactic_token
      }

      if (self.selectedTitle) {
        jsonToSend['title_code'] = self.selectedTitle.code
      }
      if (self.selectedInstructionsTemplate) {
        jsonToSend['instructions_template_code'] = self.selectedInstructionsTemplate.code
      }

      axios.post('/api/v1/components',
        JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            // Reload the page
            bus.$emit('reload-page')
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loading = true
    
    this.loadComponentPipelineOptions()
    this.loadTitleOptions()
    this.loadComponentInstructionsTemplateOptions()

    this.loading = false
  },
  computed: {
    nameError: function () {
      return _.includes(this.errors, 'name')
    },
    pipelineError: function () {
      return _.includes(this.errors, 'pipeline')
    }
  }
}