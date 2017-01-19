/* globals localStorage */

import axios from 'axios'

export default {
  name: 'AddFileFlowTemplateToComponentTemplateModal',
  props: ['componentTemplate'],
  data () {
    return {
      showModal: false,
      name: null
    }
  },
  methods: {
    submitToTactic: function () {
      var self = this

      axios.post('/api/v1/file-flow-templates',
        JSON.stringify({
          'file_flow_template': {
            'name': self.name,
            'component_template_code': self.componentTemplate.code,
          },
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            self.$router.go(self.$router.currentRoute)
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}