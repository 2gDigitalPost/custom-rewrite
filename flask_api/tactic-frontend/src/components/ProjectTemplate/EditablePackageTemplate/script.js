/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'EditablePackageTemplate',
  props: ['packageTemplate', 'platformOptions', 'pipelineOptions', 'projectTemplateCode'],
  components: {
    'multiselect': Multiselect
  },
  data () {
    return {
      editing: false,
      code: this.packageTemplate.code,
      name: this.packageTemplate.name,
      platform: this.packageTemplate.platform,
      pipeline: this.packageTemplate.pipeline
    }
  },
  methods: {
    submitChanges: function () {
      let self = this

      let jsonToSend = {
        'name': self.name,
        'package_pipeline_code': self.pipeline.code,
        'platform_code': self.platform.code,
        'project_template_code': self.projectTemplateCode,
        'token': localStorage.tactic_token
      }

      axios.post('/api/v1/package-templates/' + self.code,
        JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            // Reload the page
            bus.$emit('package-template-updated')
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}