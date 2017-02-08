/* globals localStorage */

import bus from '../../../bus'

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'InputFilesInTask',
  props: ['task', 'currentInputFiles'],
  components: {
    Multiselect,
  },
  data () {
    return {
      selectedFiles: [],
      fileOptions: [],
      loading: true,
      submitting: false
    }
  },
  methods: {
    loadFiles: function () {
      let self = this

      self.loading = true

      self.selectedFiles = self.currentInputFiles
      self.fileOptions = []

      axios.get('/api/v1/task/' + self.task.code + '/input-file-options', {
        params: {
          token: localStorage.tactic_token,
        }
      })
      .then(function (response) {
        console.log(response)
        let fileData = response.data.files

        for (let i = 0; i < fileData.length; i++) {
          self.fileOptions.push({file_path: fileData[i].file_path, code: fileData[i].code})
        }

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function () {
      let self = this

      let apiURL = '/api/v1/task/' + self.task.code + '/input-files'
      let fileCodes = _.map(self.selectedFiles, 'code')
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'file_codes': fileCodes
      }

      self.submitting = true

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          self.submitting = false

          bus.$emit('input-files-changed')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancelEdit: function () {
      bus.$emit('input-files-edit-cancel')
    }
  },
  beforeMount: function () {
    this.loadFiles()
  }
}