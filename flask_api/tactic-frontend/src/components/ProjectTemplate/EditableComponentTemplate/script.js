/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import AddFileFlowTemplateToComponentTemplateModal from '../AddFileFlowTemplateToComponentTemplateModal/index.vue'
import EditableFileFlowTemplate from '../EditableFileFlowTemplate'

import bus from '../../../bus'

export default {
  name: 'EditableComponentTemplate',
  props: ['componentTemplate', 'pipelineOptions', 'instructionsTemplateOptions', 'packageOptions', 'projectTemplateCode'],
  components: {
    'multiselect': Multiselect,
    'modal': AddFileFlowTemplateToComponentTemplateModal,
    'editable-file-flow-template': EditableFileFlowTemplate
  },
  data () {
    return {
      editing: false,
      code: this.componentTemplate.code,
      name: this.componentTemplate.name,
      pipeline: this.componentTemplate.pipeline,
      instructionsTemplate: this.componentTemplate.instructions_template,
      showModal: false
    }
  },
  methods: {
    submitChanges: function () {
      let self = this

      let jsonToSend = {
        'name': self.name,
        'component_pipeline_code': self.pipeline.code,
        'project_template_code': self.projectTemplateCode,
        'instructions_template_code': self.instructionsTemplate.code,
        'token': localStorage.tactic_token
      }

      axios.post('/api/v1/component-templates/' + self.code,
        JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            // Reload the page
            bus.$emit('component-template-updated')
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    deleteComponentTemplate: function () {
      let self = this

      let confirmation = window.confirm('Are you sure you want to delete the component "' + self.name + '"?')

      if (confirmation) {
        axios.delete('/api/v1/component-templates/' + self.code,
        {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8'
          },
          params: {
            token: localStorage.tactic_token,
          }
        })
        .then(function (response) {
          if (response.data) {
            if (response.data.status === 200) {
              bus.$emit('component-template-updated')
            }
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    }
  }
}