/* globals localStorage */

import TaskEditable from './TaskEditable/index.vue'

export default {
  name: 'TaskEditableList',
  props: ['tasks'],
  components: {
    'task-editable': TaskEditable
  }
}