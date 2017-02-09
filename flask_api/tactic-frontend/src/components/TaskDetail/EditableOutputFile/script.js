/* globals localStorage */

import bus from '../../../bus'

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'AddOutputFileToTask',
  props: ['outputFileCode', 'inputFiles'],
  components: {
    Multiselect,
  },
  data () {
    return {
      editing: false,
      name: null,
      filePath: null,
      classification: null,
      classificationOptions: ['Source', 'Intermediate', 'Deliverable'],
      selectedFiles: [],
      errors: []
    }
  },
  methods: {
    loadFile: function () {
      let self = this

      axios.get('/api/v1/file/' + self.outputFileCode, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        console.log(response)
        let fileObject = response.data.file_object

        self.name = fileObject.name
        self.filePath = fileObject.file_path
        self.classification = fileObject.classification
        self.selectedFiles = fileObject.origin_files
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function () {
      let self = this

      self.errors = []

      if (!self.name) {
        self.errors.push({type: 'name', message: 'The field "Name" is required.'})
      }
      if (!self.filePath) {
        self.errors.push({type: 'filePath', message: 'The field "Path" is required.'})
      }
      if (!self.classification) {
        self.errors.push({type: 'classification', message: 'The field "Classification" is required.'})
      }

      if (self.errors.length > 0) return

      let apiURL = '/api/v1/file/' + self.outputFileCode
      let originFileCodes = _.map(self.selectedFiles, 'code')
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'name': self.name,
        'file_path': self.filePath,
        'classification': self.classification,
        'origin_file_codes': originFileCodes
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('output-file-added')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    remove: function () {
      console.log("remove")
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
  },
  beforeMount: function () {
    this.loadFile()
  }
}