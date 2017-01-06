/* globals localStorage */

import axios from 'axios'

import bus from '../../../bus'

export default {
  name: 'FileFlowSelectable',
  props: ['fileFlow'],
  data () {
    return {
      selected: false
    }
  },
  watch: {
    selected: function () {
      bus.$emit('file-flow-selected', this.fileFlow.code, this.selected)
    }
  }
}