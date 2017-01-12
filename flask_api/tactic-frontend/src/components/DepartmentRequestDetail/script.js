/* globals localStorage */

import axios from 'axios'

export default {
  name: 'DepartmentRequestDetail',
  data () {
    return {
      departmentRequestCode: this.$route.params.code,
      departmentRequest: null,
      newStatusOptions: [],
      newStatus: null,
      response: null
    }
  },
  methods: {
    loadDepartmentRequest: function () {
      var self = this

      axios.get('/api/v1/department-requests/code/' + self.departmentRequestCode, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.departmentRequest = response.data.department_request

        let currentStatus = self.departmentRequest.summary_status

        if (currentStatus === 'Ready') {
          self.newStatusOptions = ['In Progress', 'Additional Information Needed', 'Complete']
        }
        else if (currentStatus === 'In Progress' || currentStatus === 'Revise') {
          self.newStatusOptions = ['Additional Information Needed', 'Complete']
        }
        else if (currentStatus === 'Needs Approval') {
          self.newStatusOptions = ['Rejected', 'Approved']
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitResponse: function () {
      console.log('submit')
    }
  },
  beforeMount: function () {
    this.loadDepartmentRequest()
  },
  computed: {
    responseRequired: function () {
      if (this.newStatus === null || this.newStatus === 'In Progress') return false
      else return true
    }
  }
}