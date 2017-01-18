/* globals localStorage */

import axios from 'axios'

import PackageDetail from '../PackageDetail/index.vue'

export default {
  name: 'PackageDetailList',
  props: ['packages'],
  components: {
    'package-detail': PackageDetail
  }
}