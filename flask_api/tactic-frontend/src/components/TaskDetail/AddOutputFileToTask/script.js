/* globals localStorage */

import bus from '../../../bus'

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'AddOutputFileToTask',
  props: ['task', 'inputFiles'],
  components: {
    Multiselect,
  },
  data () {
    return {
      name: null,
      selectedEquipment: [],
      equipmentOptions: [],
      loading: true,
      submitting: false
    }
  },
  methods: {
    submitToTactic: function () {
      
    }
  }
}