/* globals localStorage */

import axios from 'axios'

export default {
  name: 'InstructionsTemplatesList',
  data () {
    return {
      instructionsTemplates: []
    }
  },
  methods: {
    loadInstructionsTemplates: function () {
      var self = this

      axios.get('/api/v1/instructions-templates', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.instructionsTemplates = response.data.instructions_templates
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openInstructionsTemplateLink: function(code) {
      let url = '/instructions-templates/' + code

      this.$router.push(url)
    },
    openNewInstructionsTemplateLink: function () {
      let url = '/instructions-templates/new'

      this.$router.push(url)
    }
  },
  beforeMount: function () {
    this.loadInstructionsTemplates()
  }
}