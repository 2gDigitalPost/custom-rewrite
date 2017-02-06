/* globals localStorage */

import axios from 'axios'

export default {
  name: 'TaskTable',
  data () {
    return {
      loading: true,
      department: this.$route.params.department,
      tasks: []
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
        self.tasks = response.data.tasks

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openDetailLink (taskCode) {
      let taskDetailURL = '/task/' + taskCode

      this.$router.push(taskDetailURL)
    }
  },
  beforeMount: function () {
    this.loadTasks()

    setInterval(function () {
      this.loadTasks()
    }.bind(this), 60000)
  }
}