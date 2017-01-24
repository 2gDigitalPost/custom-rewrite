/* globals localStorage */

import ComponentEditable from './ComponentEditable/index.vue'

export default {
  name: 'ComponentEditableList',
  props: ['components'],
  components: {
    'component-editable': ComponentEditable
  }
}