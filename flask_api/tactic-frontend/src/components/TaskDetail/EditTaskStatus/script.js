/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'EditTaskStatus',
  props: ['task'],
  components: {
    Multiselect
  },
  data () {
    return {
      editingStatus: false,
      statusOptions: [],
      selectedStatus: this.task.status,
      loadingStatuses: false,
    }
  },
  methods: {
    reload: function () {
      this.editingStatus = false,
      this.selectedStatus = this.task.status,
      this.loadingStatuses = false
      this.loading = false
    },
    loadStatusOptions: function () {
      let self = this

      self.loadingStatuses = true

      axios.get('/api/v1/task/' + self.task.code + '/status-options', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.statusOptions = response.data.processes
        self.loadingStatuses = false
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
          bus.$emit('task-updated')

          self.reload()
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  watch: {
    editingStatus: function () {
      if (this.editingStatus) {
        this.loadStatusOptions()
      }
    }
  }
}