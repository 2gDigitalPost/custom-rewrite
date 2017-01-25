/* globals localStorage */

import axios from 'axios'
import marked from 'marked'

export default {
  name: 'InstructionsTemplate',
  data () {
    return {
      instructionsTemplateCode: this.$route.params.code,
      loading: false,
      instructionsTemplate: null,
    }
  },
  methods: {
    loadInstructionsTemplate: function () {
      let self = this

      self.loading = true

      axios.get('/api/v1/instructions-templates/' + self.instructionsTemplateCode, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.instructionsTemplate = response.data.instructions_template

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  computed: {
    compiledMarkdown: function () {
      return marked(this.instructionsTemplate.instructions_text, { sanitize: true })
    }
  },
  beforeMount: function () {
    this.loadInstructionsTemplate()
  }
}
