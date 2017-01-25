/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

export default {
  name: 'InstructionsTemplate',
  data () {
    return {
      instructionsTemplateCode: this.$route.params.code,
      editing: false,
      loading: false,
      instructionsTemplate: null,
      name: null,
      instructionsText: null
    }
  },
  methods: {
    loadInstructionsTemplate: function () {
      let self = this

      self.editing = false
      self.loading = true

      axios.get('/api/v1/instructions-templates/' + self.instructionsTemplateCode, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.instructionsTemplate = response.data.instructions_template
        self.name = self.instructionsTemplate.name
        self.instructionsText = self.instructionsTemplate.instructions_text

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function() {
      var self = this

      axios.post('/api/v1/instructions-templates/' + self.instructionsTemplateCode, 
        JSON.stringify({
          'name': self.name,
          'instructions_text': self.instructionsText,
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        // Reload the page
        self.loadInstructionsTemplate()
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    update: _.debounce(function (e) {
      this.instructionsText = e.target.value
    }, 300)
  },
  computed: {
    compiledMarkdown: function () {
      return marked(this.instructionsText, { sanitize: true })
    }
  },
  beforeMount: function () {
    this.loadInstructionsTemplate()
  }
}
