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

      let apiURL = '/api/v1/department-requests'

      if (self.$route.path === '/department-requests/user') {
        apiURL += '/user/' + localStorage.login
      }
      else if (self.department !== undefined) {
        apiURL += '/' + self.department
      }

      axios.get(apiURL, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.requests = response.data.department_requests
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openDetailLink (departmentRequestCode) {
      let departmentRequestDetailURL = '/department-request/' + departmentRequestCode

      this.$router.push(departmentRequestDetailURL)
    }
  },
  beforeMount: function () {
    this.loadDepartmentRequests()
  }
}