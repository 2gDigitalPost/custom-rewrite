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
  methods: {
    fileFlowSelected: function (fileFlowCode) {
      if (fileFlowCode !== this.fileFlow.code) {
        this.selected = false
      }
    }
  },
  watch: {
    selected: function () {
      bus.$emit('file-flow-selected', this.fileFlow.code, this.selected)
    }
  },
  created() {
    bus.$on('file-flow-selected', this.fileFlowSelected)
  },
  destroyed() {
    bus.$off('file-flow-selected', this.fileFlowSelected)
  }
}