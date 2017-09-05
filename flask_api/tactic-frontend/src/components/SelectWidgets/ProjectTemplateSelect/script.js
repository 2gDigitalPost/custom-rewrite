/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'ProjectTemplateSelect',
  components: {
    Multiselect,
  },
  data () {
    return {
      loading: true,
      selectedProjectTemplate: null,
      projectTemplates: []
    }
  },
  methods: {
    loadProjectTemplates: function () {
      var self = this

      axios.get('/api/v1/project-templates', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let projectTemplateData = response.data.project_templates

        self.projectTemplates = _.map(projectTemplateData, function (projectTemplate) {
          return {name: projectTemplate.name, code: projectTemplate.code}
        })
      })
      .catch(function (error) {
        console.log(error)
      })
    },
  },
  beforeMount: function () {
    this.loadProjectTemplates()
  },
  watch: {
    selectedProjectTemplate: function () {
      bus.$emit('selected-project-template-change', this.selectedProjectTemplate)
    }
  }
}