/* globals localStorage */

import axios from 'axios'

export default {
  name: 'TaskTable',
  data () {
    return {
      loading: true,
      tasks: [],
      timer: null,
      currentPage: 1,
      numberOfResultsDisplayed: 50
    }
  },
  methods: {
    loadTasks: function () {
      var self = this

      let apiURL = '/api/v1/tasks'

      if (self.$route.path === '/tasks/user') {
        apiURL += '/user/' + localStorage.login + '/assigned'
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
    },
    modifyCurrentPage: function (modifier) {
      this.currentPage += modifier
    }
  },
  computed: {
    numberOfPages: function () {
      return Math.ceil(this.tasks.length / this.numberOfResultsDisplayed)
    },
    displayedTasks: function () {
      return this.tasks.slice((this.currentPage - 1) * this.numberOfResultsDisplayed, (this.currentPage * this.numberOfResultsDisplayed))
    },
    department: function () {
      return this.$route.params.department
    },
    pageTitle: function () {
      if (this.$route.path === '/tasks/user') {
        return 'My Tasks'
      }
      else if (this.department) {
        return _.startCase(this.department) + ' Tasks'
      }
      else {
        return 'Tasks'
      }
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
  },
  watch: {
    '$route': function () {
      this.loadTasks()
    }
  },
}