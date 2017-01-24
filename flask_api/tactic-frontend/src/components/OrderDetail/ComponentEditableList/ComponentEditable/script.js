/* globals localStorage */

import axios from 'axios'

import EditableTitle from './EditableTitle/index.vue'

export default {
  name: 'ComponentEditable',
  props: ['component'],
  components: {
    EditableTitle
  },
  data () {
    return {
      componentObject: this.component.component,
      fileFlowToComponents: this.component.file_flow_to_component,
      fileFlows: this.component.file_flows,
      tasks: this.component.tasks,
      title: this.component.title
    }
  }
}