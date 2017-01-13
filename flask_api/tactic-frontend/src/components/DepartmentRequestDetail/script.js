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
      requestResponse: null,
      responseRequired: false
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
        else if (currentStatus === 'Additional Info Needed') {
          self.newStatusOptions = ['Ready']
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
      var self = this

      let jsonToSubmit = {
        'department_request': {
          'search_key': self.departmentRequest['__search_key__'],
          'status': self.newStatus
        },
        'token': localStorage.tactic_token
      }

      if (self.responseRequired) {
        jsonToSubmit['department_request']['response'] = self.requestResponse
      }

      axios.post('/api/v1/department-requests/code/' + self.departmentRequestCode,
        JSON.stringify(jsonToSubmit), {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8'
          }
        }
      )
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
  },
  beforeMount: function () {
    this.loadDepartmentRequest()
  },
  watch: {
    newStatus: function () {
      if (this.newStatus === null || this.newStatus === 'In Progress') {
        this.responseRequired = false
      }
      else {
        this.responseRequired = true
      }
    }
  },
  computed: {
    displaySubmitButton: function () {
      if (this.newStatus === null) return false
      if (this.responseRequired === true && (this.requestResponse === '' || this.requestResponse === null)) return false

      return true
    }
  }
}