/* globals localStorage */

import _ from 'lodash'
import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../bus'

export default {
  name: 'NewFileForm',
  props: ['files', 'orderCode'],
  components: {
    Multiselect
  },
  data () {
    return {
      newFileName: null,
      newFilePath: null,
      newFileClassification: null,
      classificationOptions: ['Source', 'Intermediate', 'Deliverable'],
      selectedFiles: [],
      errors: []
    }
  },
  methods: {
    submitNewFile: function () {
      let self = this

      self.errors = []

      if (!self.newFileName) {
        self.errors.push({type: 'name', message: 'The field "Name" is required.'})
      }
      if (!self.newFilePath) {
        self.errors.push({type: 'filePath', message: 'The field "Path" is required.'})
      }
      if (!self.newFileClassification) {
        self.errors.push({type: 'classification', message: 'The field "Classification" is required.'})
      }

      if (self.errors.length > 0) return

      let apiURL = '/api/v1/file'
      let originFileCodes = _.map(self.selectedFiles, 'code')
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'file': {
          'name': self.newFileName,
          'file_path': self.newFilePath,
          'classification': self.newFileClassification
        },
        'order_code': self.orderCode,
        'origin_file_codes': originFileCodes
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('new-file-added-to-order')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancel: function () {
      bus.$emit('new-file-entry-cancel')
    }
  },
  computed: {
    nameError: function () {
      return _.includes(_.map(this.errors, 'type'), 'name')
    },
    filePathError: function () {
      return _.includes(_.map(this.errors, 'type'), 'filePath')
    },
    classificationError: function () {
      return _.includes(_.map(this.errors, 'type'), 'classification')
    }
  }
}