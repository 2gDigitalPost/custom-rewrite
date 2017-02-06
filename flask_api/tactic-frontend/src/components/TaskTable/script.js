/* globals localStorage */

import axios from 'axios'

export default {
  name: 'TaskTable',
  data () {
    return {
      loading: true,
      department: this.$route.params.department,
      tasks: [],
      timer: null
    }
  },
  methods: {
    loadTasks: function () {
      var self = this

      let apiURL = '/api/v1/tasks'

      if (self.$route.path === '/tasks/user') {
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
        self.tasks = self.sortByDueDate(response.data.tasks)

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openDetailLink: function (taskCode) {
      let taskDetailURL = '/task/' + taskCode

      this.$router.push(taskDetailURL)
    },
    sortByDueDate: function (taskObjects) {
      return _.sortBy(taskObjects, 'bid_end_date')
    }
  },
  beforeMount: function () {
    this.loadTasks()
  },
  created: function () {
    this.timer = setInterval(function () {
      this.loadTasks()
    }.bind(this), 60000)
  },
  destroyed: function () {
    clearInterval(this.timer)
  }
}