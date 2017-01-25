/* globals localStorage */

import axios from 'axios'
import marked from 'marked'

export default {
  name: 'NewInstructionsTemplate',
  data () {
    return {
      name: null,
      instructionsText: '# hello',
    }
  },
  methods: {
    submitToTactic: function() {
      var self = this

      axios.post('/api/v1/instructions-templates', 
        JSON.stringify({
          'name': self.name,
          'instructions_text': self.instructionsText,
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.$router.push('/instructions-templates/' + response.data.code)
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
  }
}