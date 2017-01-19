/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'EditableFileFlowTemplate',
  props: ['fileFlowTemplate'],
  components: {
    'multiselect': Multiselect
  },
  data () {
    return {
      editing: false,
      code: this.fileFlowTemplate.code,
      name: this.fileFlowTemplate.name,
    }
  }
}
