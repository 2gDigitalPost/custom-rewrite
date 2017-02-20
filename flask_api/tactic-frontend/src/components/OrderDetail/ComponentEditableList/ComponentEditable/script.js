/* globals localStorage */

import axios from 'axios'

import EditableTitle from './EditableTitle/index.vue'
import TaskEditableList from './TaskEditableList/index.vue'
import FileFlowEditableList from '../../../FileFlowEditableList/index.vue'

export default {
  name: 'ComponentEditable',
  props: ['component'],
  components: {
    EditableTitle,
    TaskEditableList,
    FileFlowEditableList
  },
  data () {
    return {
      componentObject: this.component.component,
      fileFlows: this.component.file_flows,
      tasks: this.component.tasks,
      title: this.component.title,
      instructionsDocument: this.component
    }
  },
  methods: {
    loadInstructionsPage: function () {
      let instructionsPageURL = '/instructions/' + this.component.component.instructions_code

      this.$router.push(instructionsPageURL)
    }
  }
}