/* globals localStorage */

import axios from 'axios'

import bus from '../../bus'

export default {
  name: 'TaskDetail',
  data () {
    return {
      taskCode: this.$route.params.code,
      taskObject: null,
    }
  }
}