/* globals localStorage */

import axios from 'axios'

export default {
  name: 'NewProjectTemplateForm',
  data () {
    return {
      name: null,
    }
  },
  methods: {
    submitToTactic: function() {
      var self = this

      axios.post('/api/v1/project-templates', 
        JSON.stringify({
          'name': self.name,
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            // Redirect to the project template edit page
            self.$router.push('/project-templates/' + response.data.project_template_code)
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}