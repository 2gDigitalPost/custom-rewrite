/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../../bus'

export default {
  name: 'EditableFileFlowTemplate',
  props: ['fileFlowTemplate', 'packageOptions'],
  data () {
    return {
      editing: false,
      code: this.fileFlowTemplate.code,
      name: this.fileFlowTemplate.name,
      checkedOptions: [],
      connectedPackages: this.fileFlowTemplate.connected_packages,
      connectedPackagesNames: []
    }
  },
  methods: {
    setupPackageNames: function () {
      this.connectedPackagesNames = []

      for (let i = 0; i < this.connectedPackages.length; i++) {
        for (let j = 0; j < this.packageOptions.length; j++) {
          if (this.connectedPackages[i] === this.packageOptions[j].code) {
            this.connectedPackagesNames.push(this.packageOptions[j].name)
          }
        }
      }
    },
    setupCheckedOptions: function () {
      this.checkedOptions = []

      for (let i = 0; i < this.connectedPackages.length; i++) {
        this.checkedOptions.push(this.connectedPackages[i])
      }
    },
    submitChanges: function () {
      let self = this

      let newPackageConnections = _.difference(self.checkedOptions, self.connectedPackages)
      let deletedPackageConnections = _.difference(self.connectedPackages, self.checkedOptions)

      if (newPackageConnections.length > 0 || deletedPackageConnections.length > 0) {
        axios.post('/api/v1/file-flow-templates/' + self.code + '/package-templates',
          JSON.stringify({
            'new_package_connections': newPackageConnections,
            'deleted_package_connections': deletedPackageConnections,
            'token': localStorage.tactic_token
          }), {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8'
          },
        })
        .then(function (response) {
          if (response.data) {
            if (response.data.status === 200) {
              bus.$emit('file-flow-template-updated')
            }
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    },
    deleteFileFlowTemplate: function () {
      let self = this

      let confirmation = window.confirm('Are you sure you want to delete the file flow "' + self.name + '"?')

      if (confirmation) {
        axios.delete('/api/v1/file-flow-templates/' + self.code,
        {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8'
          },
          params: {
            token: localStorage.tactic_token,
          }
        })
        .then(function (response) {
          if (response.data) {
            if (response.data.status === 200) {
              bus.$emit('file-flow-template-updated')
            }
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    }
  },
  beforeMount: function () {
    this.setupPackageNames()
  },
  watch: {
    editing: function () {
      this.setupCheckedOptions()
    }
  }
}
