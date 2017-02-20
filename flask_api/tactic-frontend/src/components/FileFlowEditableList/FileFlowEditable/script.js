/* globals localStorage */

import axios from 'axios'

export default {
  name: 'FileFlowEditable',
  props: ['fileFlow'],
  data () {
    return {
      fileObject: this.fileFlow.file_object,
      editing: false,
      editName: null,
      editDeliveringTo: [],
      editFileObject: null
    }
  }
}