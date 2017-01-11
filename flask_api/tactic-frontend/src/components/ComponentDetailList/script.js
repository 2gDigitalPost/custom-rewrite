/* globals localStorage */

import axios from 'axios'

import ComponentDetail from '../ComponentDetail/index.vue'

export default {
  name: 'ComponentDetailList',
  props: ['components', 'componentsFull'],
  components: {
    'component-detail': ComponentDetail
  }
}