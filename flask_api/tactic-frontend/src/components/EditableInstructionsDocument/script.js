/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

export default {
  name: 'EditableInstructionsDocument',
  data () {
    return {
      instructionsCode: null,
      editing: false,
      splitting: false,
      loading: true,
      instructionsDocument: null,
      name: null,
      currentInstructionsText: null,
      newInstructionsText: null,
      components: [],
      selectedComponents: []
    }
  },
  methods: {
    loadInstructionsDocument: function () {
      let self = this

      self.instructionsCode = this.$route.params.code

      self.editing = false
      self.splitting = false
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
        self.components = self.instructionsDocument.components
        self.selectedComponents = []

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function() {
      let self = this

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
    submitSplitInstructions: function () {
      let self = this

      axios.post('/api/v1/instructions/components', JSON.stringify({
        'name': self.name,
        'instructions_text': self.currentInstructionsText,
        'component_codes': self.selectedComponents,
        'token': localStorage.tactic_token
      }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        let newInstructionsCode = response.data.new_instructions_code

        // Load the page for the new document
        self.$router.push('/instructions/' + newInstructionsCode)
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    toggleSelectedComponent: function (componentCode) {
      if (this.componentSelected(componentCode)) {
        this.selectedComponents.splice(this.selectedComponents.indexOf(componentCode), 1)
      }
      else {
        this.selectedComponents.push(componentCode)
      }
    },
    componentSelected: function (componentCode) {
      if (_.includes(this.selectedComponents, componentCode)) return true
      else return false
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
  watch: {
    editing: function () {
      if (this.editing) {
        this.splitting = false
      }
    },
    splitting: function () {
      if (this.splitting) {
        this.editing = false
      }
    },
    '$route.params.code': function () {
      this.loadInstructionsDocument()
    }
  },
  beforeMount: function () {
    this.loadInstructionsDocument()
  },
}