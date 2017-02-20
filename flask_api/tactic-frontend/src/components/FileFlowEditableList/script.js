/* globals localStorage */

import FileFlowEditable from './FileFlowEditable/index.vue'

export default {
  name: 'FileFlowEditableList',
  props: ['fileFlows', 'componentStatus'],
  components: {
    FileFlowEditable
  }
}