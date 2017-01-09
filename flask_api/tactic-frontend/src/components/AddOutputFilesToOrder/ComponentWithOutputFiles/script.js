/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../../bus'

export default {
  name: 'ComponentWithOutputFiles',
  props: ['component', 'selected', 'externallySelected'],
  methods: {
    componentSelected: function () {
      bus.$emit('component-selected', this.component.code)
    }
  },
  created() {
    bus.$on('highlight-components', this.fileFlowSelected)
  },
  destroyed() {
    bus.$off('highlight-components', this.fileFlowSelected)
  }
}