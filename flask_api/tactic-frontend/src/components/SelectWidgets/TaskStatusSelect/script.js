/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'TaskStatusSelect',
  props: ['task'],
  components: {
    Multiselect
  },
  data () {
    return {
      statusOptions: [],
      selectedStatus: this.task.status,
      loading: false,
    }
  },
  methods: {
    reload: function () {
      this.selectedStatus = this.task.status,
      this.loading = false
    },
    loadStatusOptions: function () {
      let self = this

      self.loading = true

      axios.get('/api/v1/task/' + self.task.code + '/status-options', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.statusOptions = response.data.processes
        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadStatusOptions()
  },
  watch: {
    selectedStatus: function () {
      bus.$emit('selected-status-change', this.selectedStatus)
    }
  }
}