/* globals localStorage */

import PackageEditable from './PackageEditable/index.vue'

export default {
  name: 'PackageEditableList',
  props: ['packages'],
  components: {
    PackageEditable
  }
}