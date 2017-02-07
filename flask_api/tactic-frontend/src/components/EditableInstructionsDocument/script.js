/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

export default {
  name: 'EditableInstructionsDocument',
  data () {
    return {
      instructionsCode: this.$route.params.code,
      editing: false,
      loading: true,
      instructionsDocument: null,
      name: null,
      currentInstructionsText: null,
      newInstructionsText: null
    }
  },
  methods: {
    loadInstructionsDocument: function () {
      let self = this

      self.editing = false
      self.loading = true

      axios.get('/api/v1/instructions/' + self.instructionsCode, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.instructionsDocument = response.data.instructions
        self.name = self.instructionsDocument.name
        self.currentInstructionsText = self.instructionsDocument.instructions_text
        self.newInstructionsText = self.currentInstructionsText

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function() {
      var self = this

      axios.post('/api/v1/instructions/' + self.instructionsCode, 
        JSON.stringify({
          'name': self.name,
          'instructions_text': self.newInstructionsText,
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        // Reload the page
        self.loadInstructionsDocument()
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    update: _.debounce(function (e) {
      this.newInstructionsText = e.target.value
    }, 300)
  },
  computed: {
    currentCompiledMarkdown: function () {
      return marked(this.currentInstructionsText, { sanitize: true })
    },
    newCompiledMarkdown: function () {
      return marked(this.newInstructionsText, { sanitize: true })
    }
  },
  beforeMount: function () {
    this.loadInstructionsDocument()
  }
}