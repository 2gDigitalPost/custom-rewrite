/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../../bus'

export default {
  name: 'ComponentWithOutputFiles',
  props: ['component'],
  data () {
    return {
      selected: false,
      externallySelected: false
    }
  },
  methods: {
    /*
    fileFlowSelected: function (componentCode) {
      if (componentCode == this.component.code) {
        this.externallySelected = true
      }
      else {
        this.externallySelected = false
      }
    }
    */
    fileFlowSelected: function (componentCodes) {
      // if (componentCodes.contains(this.component.code)) {
      if (_.includes(componentCodes, this.component.code)) {
        this.externallySelected = true
      }
      else {
        this.externallySelected = false
      }
    }
  },
  created() {
    // bus.$on('highlight-component', this.fileFlowSelected)
    bus.$on('highlight-components', this.fileFlowSelected)
  },
  destroyed() {
    // bus.$off('highlight-component', this.fileFlowSelected)
    bus.$off('highlight-components', this.fileFlowSelected)
  }
}