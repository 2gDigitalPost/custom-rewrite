/* globals localStorage */

import _ from 'lodash'
import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../bus'

export default {
  name: 'ImportFileToOrder',
  props: ['divisionCode', 'orderCode', 'importedFiles'],
  components: {
    Multiselect
  },
  data () {
    return {
      loading: true,
      divisionFiles: [],
      classificationOptions: ['Source', 'Intermediate', 'Deliverable'],
      selectedFiles: [],
      errors: []
    }
  },
  methods: {
    loadDivisionFiles: function () {
      let self = this
      self.loading = true

      axios.get('/api/v1/division/' + self.divisionCode + '/files', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.divisionFiles = self.filterFileOptions(response.data.files)
        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    filterFileOptions: function (fileOptions) {
      let importedFileCodes = _.map(this.importedFiles, 'code')

      return _.reject(fileOptions, function (fileOption) {
        return _.includes(importedFileCodes, fileOption['code'])
      })
    },
    submitFileImport: function () {
      let self = this

      let apiURL = '/api/v1/files-in-order'
      let selectedFileCodes = _.map(self.selectedFiles, 'code')
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'order_code': self.orderCode,
        'file_codes': selectedFileCodes
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('files-imported')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancel: function () {
      bus.$emit('file-import-cancel')
    }
  },
  beforeMount: function () {
    this.loadDivisionFiles()
  }
}
