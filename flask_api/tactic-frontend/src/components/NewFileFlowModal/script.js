/* globals localStorage */

import axios from 'axios'

export default {
  name: 'NewFileFlowModal',
  props: ['orderCode'],
  data () {
    return {
      showModal: false,
      name: null
    }
  },
  methods: {
    submitToTactic: function () {
      var self = this

      axios.post('/api/v1/file-flows', 
        JSON.stringify({
          'file_flow': {
            'name': self.name,
            'order_code': self.orderCode
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