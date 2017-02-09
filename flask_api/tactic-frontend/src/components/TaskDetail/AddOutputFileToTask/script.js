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
      filePath: null,
      classification: null,
      classificationOptions: ['Source', 'Intermediate', 'Deliverable'],
      selectedFiles: [],
      errors: []
    }
  },
  methods: {
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

      let apiURL = '/api/v1/task/' + self.task.code + '/output-file'
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
    cancelEdit: function () {
      bus.$emit('add-output-file-cancel')
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