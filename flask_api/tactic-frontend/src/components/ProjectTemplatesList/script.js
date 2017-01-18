/* globals localStorage */

import axios from 'axios'

export default {
  name: 'ProjectTemplatesList',
  data () {
    return {
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
        self.projectTemplates = response.data.project_templates
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openProjectTemplateLink: function(code) {
      let url = '/project-templates/' + code

      this.$router.push(url)
    },
    openNewProjectTemplateLink: function () {
      let url = '/project-templates/new'

      this.$router.push(url)
    }
  },
  beforeMount: function () {
    this.loadProjectTemplates()
  }
}