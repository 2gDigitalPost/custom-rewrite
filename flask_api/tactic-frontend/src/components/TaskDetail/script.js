/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../bus'

export default {
  name: 'TaskDetail',
  data () {
    return {
      taskObject: null,
      taskDataObject: null,
      inputTasks: [],
      outputTasks: [],
      editingStatus: false,
    }
  },
  methods: {
    loadTask: function () {
      let self = this

      let taskCodeParam = self.$route.params.code

      self.taskObject = null
      self.taskDataObject = null
      self.inputTasks = []
      self.outputTasks = []

      axios.get('/api/v1/tasks/' + taskCodeParam + '/full', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.taskObject = response.data.task
        self.taskDataObject = response.data.task_data
        self.inputTasks = response.data.input_tasks
        self.outputTasks = response.data.output_tasks
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    setupTaskLinks: function (taskList) {
      let links = []

      _.forEach(taskList, function (task) {
        links.push({name: task.process, url: '/tasks/' + task.code})
      })

      return links
    }
  },
  beforeMount: function () {
    this.loadTask()
  },
  computed: {
    inputTaskLinks: function () {
      return this.setupTaskLinks(this.inputTasks)
    },
    outputTaskLinks: function () {
      return this.setupTaskLinks(this.outputTasks)
    }
  },
  watch: {
    '$route': function () {
      this.loadTask()
    }
  }
}