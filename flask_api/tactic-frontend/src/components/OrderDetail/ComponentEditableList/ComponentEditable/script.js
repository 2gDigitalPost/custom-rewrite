/* globals localStorage */

import axios from 'axios'

import EditableTitle from './EditableTitle/index.vue'
import TaskEditableList from './TaskEditableList/index.vue'

export default {
  name: 'ComponentEditable',
  props: ['component'],
  components: {
    EditableTitle,
    TaskEditableList
  },
  data () {
    return {
      componentObject: this.component.component,
      fileFlowToComponents: this.component.file_flow_to_component,
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