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
    fileFlowSelected: function (componentCodes, selected) {
      if (_.includes(componentCodes, this.component.code)) {
        this.externallySelected = selected
      }
    }
  },
  created() {
    bus.$on('highlight-components', this.fileFlowSelected)
  },
  destroyed() {
    bus.$off('highlight-components', this.fileFlowSelected)
  }
}