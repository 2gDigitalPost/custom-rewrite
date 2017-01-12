/* globals localStorage */

import axios from 'axios'

export default {
  name: 'DepartmentRequestTable',
  data () {
    return {
      department: this.$route.params.department,
      requests: []
    }
  },
  methods: {
    loadDepartmentRequests: function () {
      var self = this

      axios.get('/api/v1/department-requests/' + self.department, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        console.log(response)

        self.requests = response.data.department_requests
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadDepartmentRequests()
  }
}