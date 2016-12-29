/* globals localStorage */

import axios from 'axios'

export default {
  name: 'OrderDetail',
  data () {
    return {
      order_code: this.$route.params.code,
      titles: []
    }
  },
}