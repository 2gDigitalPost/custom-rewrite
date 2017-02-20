/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'FileFlowEditable',
  props: ['fileFlow', 'componentStatus'],
  data () {
    return {
      fileObject: this.fileFlow.file_object,
      editing: false,
      editName: null,
      editDeliveringTo: [],
      editFileObject: null
    }
  },
  computed: {
    componentCompleteError: function () {
      if (this.componentStatus.toLowerCase() === 'complete') return true
      else return false
    }
  }
}