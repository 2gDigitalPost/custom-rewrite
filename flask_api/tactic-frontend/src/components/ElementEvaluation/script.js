/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'ElementEvaluation',
  components: {
    Multiselect
  },
  data () {
    return {
      code: this.$route.params.code,
      loading: false,
    }
  },
  methods: {
    
  }
}