/* globals localStorage */

import ComponentEntryForm from './ComponentEntryForm/index.vue'
import ComponentEditable from './ComponentEditable/index.vue'

export default {
  name: 'ComponentEditableList',
  props: ['components', 'orderCode'],
  components: {
    ComponentEntryForm,
    ComponentEditable
  },
  data () {
    return {
      addingComponent: false,
    }
  }
}