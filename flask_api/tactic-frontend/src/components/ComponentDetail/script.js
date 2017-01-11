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
  },
  methods: {
    loadTitle: function (titleCode) {
      console.log(this.componentFull)

      if (titleCode === null) return null


    }
  },
  beforeMount: function () {
    this.loadTitle(this.component.title_code)
  }
}