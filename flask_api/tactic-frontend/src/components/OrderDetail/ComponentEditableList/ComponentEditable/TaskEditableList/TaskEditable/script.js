/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../../../../bus'

export default {
  name: 'TaskEditable',
  props: ['task'],
  components: {
    Multiselect
  },
  data () {
    return {
      editing: false,
      loading: false,
    }
  }
}