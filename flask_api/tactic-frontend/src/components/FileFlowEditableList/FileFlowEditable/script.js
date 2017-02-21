/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'FileFlowEditable',
  props: ['fileFlow', 'componentStatus'],
  components: {
    Multiselect
  },
  data () {
    return {
      fileObject: this.fileFlow.file_object,
      loading: false,
      editing: false,
      editName: this.fileFlow.name,
      editDeliveringTo: [],
      editFileObject: null,
      packageOptions: [],
      deliverableFileOptions: [],
      selectedFile: this.fileFlow.file_object
    }
  },
  methods: {
    loadAll: function () {
      let self = this
      self.loading = true

      let fileFlowCode = self.fileFlow.code
      axios.all([self.loadPackages(fileFlowCode), self.loadDeliverableFiles(fileFlowCode)])
        .then(axios.spread(function (packagesResponse, deliverableFilesResponse) {
          self.packageOptions = packagesResponse.data.packages
          self.deliverableFileOptions = deliverableFilesResponse.data.files
          self.setupCheckedOptions()
          self.loading = false
        }));
    },
    loadPackages: function (fileFlowCode) {
      return axios.get('/api/v1/file-flow/' + fileFlowCode + '/package-options', {
        params: {
          token: localStorage.tactic_token
        }
      })
    },
    loadDeliverableFiles: function (fileFlowCode) {
      return axios.get('/api/v1/file-flow/' + fileFlowCode + '/deliverable-file-options', {
        params: {
          token: localStorage.tactic_token
        }
      })
    },
    setupCheckedOptions: function () {
      this.editDeliveringTo = []

      for (let i = 0; i < this.fileFlow.delivering_to.length; i++) {
        this.editDeliveringTo.push(this.fileFlow.delivering_to[i].code)
      }
    },
    submitChanges: function () {
      let self = this

      let updateData = {}

      if (self.editName !== self.fileFlow.name) {
        updateData['name'] = self.editName
      }

      let currentPackageConnectionCodes = _.map(self.fileFlow.delivering_to, 'code')

      let newPackageConnections = _.difference(self.editDeliveringTo, currentPackageConnectionCodes)
      let deletedPackageConnections = _.difference(currentPackageConnectionCodes, self.editDeliveringTo)

      if (newPackageConnections.length > 0) {
        updateData['new_package_connections'] = newPackageConnections
      }

      if (deletedPackageConnections.length > 0) {
        updateData['deleted_package_connections'] = deletedPackageConnections
      }

      if (self.selectedFile !== null && self.selectedFile.code !== self.fileFlow.file_code) {
        updateData['file_code'] = self.selectedFile.code
      }

      let apiURL = '/api/v1/file-flow/' + self.fileFlow.code
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
          bus.$emit('file-flow-updated')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  computed: {
    componentCompleteError: function () {
      if (this.componentStatus.toLowerCase() === 'complete') return true
      else return false
    }
  },
  watch: {
    editing: function () {
      if (this.editing) {
        this.loadAll()
      }
    }
  }
}