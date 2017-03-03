/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../bus'

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
        console.log(response)
        self.statusOptions = response.data.processes
        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitStatusChangeToTactic: function () {
      let self = this

      let apiURL = '/api/v1/task/' + self.task.code

      let updateData = {'status': self.selectedStatus}
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'update_data': updateData
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('reload-page')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancelEdit: function () {
      bus.$emit('task-status-edit-cancel')
    }
  },
  beforeMount: function () {
    this.loadStatusOptions()
  }
}