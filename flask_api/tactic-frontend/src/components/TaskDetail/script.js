/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

import bus from '../../bus'

import EquipmentInTask from './EquipmentInTask/index.vue'
import InputFilesInTask from './InputFilesInTask/index.vue'
import AddOutputFileToTask from './AddOutputFileToTask/index.vue'
import EditableEstimatedHours from '../EditableEstimatedHours/index.vue'
import EditableOutputFile from './EditableOutputFile/index.vue'
import EditTaskStatus from './EditTaskStatus/index.vue'
import FileFlowInTaskList from './FileFlowInTaskList/index.vue'
import OutputFilesInTask from './OutputFilesInTask/index.vue'

export default {
  name: 'TaskDetail',
  components: {
    EquipmentInTask,
    InputFilesInTask,
    AddOutputFileToTask,
    OutputFilesInTask,
    EditableEstimatedHours,
    EditableOutputFile,
    EditTaskStatus,
    FileFlowInTaskList
  },
  data () {
    return {
      taskObject: null,
      taskDataObject: null,
      parent: null,
      order: null,
      instructionsText: null,
      inputTasks: [],
      outputTasks: [],
      estimatedHours: null,
      equipment: [],
      inputFiles: [],
      outputFiles: [],
      editingStatus: false,
      editingEquipment: false,
      editingInputFiles: false,
      addingOutputFile: false,
      importingOutputFiles: false
    }
  },
  methods: {
    loadTask: function () {
      let self = this

      let taskCodeParam = self.$route.params.code

      self.taskObject = null
      self.taskDataObject = null
      self.parent = null
      self.order = null
      self.instructionsText = null
      self.inputTasks = []
      self.outputTasks = []
      self.estimatedHours = null
      self.equipment = []
      self.inputFiles = []
      self.outputFiles = []
      self.editingStatus = false
      self.editingEquipment = false
      self.editingInputFiles = false
      self.addingOutputFile = false
      self.importingOutputFiles = false

      axios.get('/api/v1/task/' + taskCodeParam + '/full', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.taskObject = response.data.task
        self.taskDataObject = response.data.task_data
        self.parent = response.data.parent
        self.order = response.data.order
        self.instructionsText = response.data.instructions_text
        self.inputTasks = response.data.input_tasks
        self.outputTasks = response.data.output_tasks
        self.estimatedHours = response.data.task_data.estimated_hours
        self.equipment = response.data.equipment
        self.inputFiles = response.data.input_files
        self.outputFiles = response.data.output_files
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    setupTaskLinks: function (taskList) {
      let links = []

      _.forEach(taskList, function (task) {
        links.push({name: task.process, url: '/task/' + task.code})
      })

      return links
    },
    cancelEquipmentEdit: function () {
      this.editingEquipment = false
    },
    cancelInputFilesEdit: function () {
      this.editingInputFiles = false
    },
    cancelOutputFilesEdit: function () {
      this.importingOutputFiles = false
    },
    cancelAddOutputFile: function () {
      this.addingOutputFile = false
    },
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
    },
    orderLink: function () {
      if (this.order) {
        return '/orders/' + this.order.code
      }
      else {
        return null
      }
    }
  },
  watch: {
    '$route': function () {
      this.loadTask()
    }
  },
  created() {
    bus.$on('equipment-edit-cancel', this.cancelEquipmentEdit)
    bus.$on('equipment-changed', this.loadTask)
    bus.$on('input-files-edit-cancel', this.cancelInputFilesEdit)
    bus.$on('input-files-changed', this.loadTask)
    bus.$on('output-files-edit-cancel', this.cancelOutputFilesEdit)
    bus.$on('output-files-changed', this.loadTask)
    bus.$on('add-output-file-cancel', this.cancelAddOutputFile)
    bus.$on('output-file-added', this.loadTask)
    bus.$on('task-updated', this.loadTask)
    bus.$on('estimated-hours-updated', this.loadTask)
    bus.$on('file-flow-updated', this.loadTask)
  },
  destroyed() {
    bus.$off('equipment-edit-cancel', this.cancelEquipmentEdit)
    bus.$off('equipment-changed', this.loadTask)
    bus.$off('input-files-edit-cancel', this.cancelInputFilesEdit)
    bus.$off('input-files-changed', this.loadTask)
    bus.$off('output-files-edit-cancel', this.cancelOutputFilesEdit)
    bus.$off('output-files-changed', this.loadTask)
    bus.$off('add-output-file-cancel', this.cancelAddOutputFile)
    bus.$off('output-file-added', this.loadTask)
    bus.$off('task-updated', this.loadTask)
    bus.$off('estimated-hours-updated', this.loadTask)
    bus.$off('file-flow-updated', this.loadTask)
  },
}