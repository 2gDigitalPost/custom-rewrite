/* globals localStorage */

import axios from 'axios'

export default {
  name: 'ComponentDetail',
  props: ['componentFull'],
  data () {
    return {
      component: this.componentFull.component,
      fileFlowToComponents: this.componentFull.file_flow_to_component,
      fileFlows: this.componentFull.file_flows,
      tasks: this.componentFull.tasks,
      title: this.componentFull.title
    }
  }
}