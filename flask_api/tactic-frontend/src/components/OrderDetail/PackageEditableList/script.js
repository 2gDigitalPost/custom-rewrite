/* globals localStorage */

import PackageEntryForm from './PackageEntryForm/index.vue'
import PackageEditable from './PackageEditable/index.vue'

export default {
  name: 'PackageEditableList',
  props: ['packages', 'orderCode'],
  components: {
    PackageEntryForm,
    PackageEditable
  },
  data () {
    return {
      addingPackage: false
    }
  }
}