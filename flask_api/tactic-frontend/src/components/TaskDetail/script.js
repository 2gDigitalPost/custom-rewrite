/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

import bus from '../../bus'

export default {
  name: 'TaskDetail',
  data () {
    return {
      taskObject: null,
      taskDataObject: null,
      parent: null,
      instructionsText: null,
      inputTasks: [],
      outputTasks: [],
      equipment: [],
      editingStatus: false,
    }
  },
  methods: {
    loadTask: function () {
      let self = this

      let taskCodeParam = self.$route.params.code

      self.taskObject = null
      self.taskDataObject = null
      self.parent = null
      self.instructionsText = null
      self.inputTasks = []
      self.outputTasks = []
      self.equipment = []

      axios.get('/api/v1/tasks/' + taskCodeParam + '/full', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.taskObject = response.data.task
        self.taskDataObject = response.data.task_data
        self.parent = response.data.parent
        self.instructionsText = response.data.instructions_text
        self.inputTasks = response.data.input_tasks
        self.outputTasks = response.data.output_tasks
        self.equipment = response.data.equipment
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
    },
    compiledMarkdown: function () {
      return marked(this.instructionsText, { sanitize: true })
    }
  },
  watch: {
    '$route': function () {
      this.loadTask()
    }
  }
}