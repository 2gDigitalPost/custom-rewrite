/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../../../bus'

export default {
  name: 'FileEditable',
  props: ['file', 'orderCode', 'fileOptions'],
  components: {
    Multiselect
  },
  data () {
    return {
      editing: false,
      editName: null,
      editPath: null,
      editClassification: null,
      classificationOptions: ['Source', 'Intermediate', 'Deliverable'],
      selectedFiles: [],
      errors: []
    }
  },
  methods: {
    loadValues: function () {
      let self = this

      self.editName = self.file.name
      self.editPath = self.file.file_path
      self.editClassification = _.startCase(self.file.classification)

      axios.get('/api/v1/file/' + self.file.code, {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        console.log(response)
        self.selectedFiles = response.data.file_object.origin_files
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitChanges: function () {
      let self = this

      self.errors = []

      if (!self.editName) {
        self.errors.push({type: 'name', message: 'The field "Name" is required.'})
      }
      if (!self.editPath) {
        self.errors.push({type: 'filePath', message: 'The field "Path" is required.'})
      }
      if (!self.editClassification) {
        self.errors.push({type: 'classification', message: 'The field "Classification" is required.'})
      }

      let fileJSON = {}

      if (self.editName !== self.file.name) {
        fileJSON['name'] = self.editName
      }
      if (self.editPath !== self.file.file_path) {
        fileJSON['file_path'] = self.editPath
      }
      if (self.editClassification !== _.startCase(self.file.classification)) {
        fileJSON['classification'] = self.editClassification
      }
      
      if (_.keysIn(fileJSON).length === 0) {
        self.errors.push({type: 'noChanges', message: 'No changes have been made!'})
      }

      if (self.errors.length > 0) return

      let apiURL = '/api/v1/file/' + self.file.code
      let originFileCodes = _.map(self.selectedFiles, 'code')
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'file': fileJSON,
        'origin_file_codes': originFileCodes
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('file-updated')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    removeFileFromOrder: function () {
      let self = this
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
    },
    noChangesError: function () {
      return _.includes(_.map(this.errors, 'type'), 'noChanges')
    }
  },
  watch: {
    editing: function () {
      if (this.editing) {
        this.loadValues()
      }
    }
  }
}