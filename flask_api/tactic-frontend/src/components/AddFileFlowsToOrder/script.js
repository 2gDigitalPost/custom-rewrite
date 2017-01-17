/* globals localStorage */

import _ from 'lodash'
import axios from 'axios'

import AddFileFlowToComponentModal from './AddFileFlowToComponentModal/index.vue'

export default {
  name: 'AddFileFlowsToOrder',
  components: {
    'modal': AddFileFlowToComponentModal
  },
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      components: [],
      selectable_packages: [],
      changes: [],
      selectedFileFlow: null,
      fileFlows: [],
      fileFlowToPackages: [],
      showModal: []
    }
  },
  methods: {
    loadOrder: function () {
      var self = this

      axios.get('/api/v1/orders/' + self.order_code + '/full', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let orderData = response.data.order
        let componentsData = response.data.components_full
        let packagesData = response.data.packages

        self.order_sobject = orderData
        self.order_name = orderData['name']

        for (let i = 0; i < componentsData.length; i++) {
          self.components.push({
            'component': componentsData[i],
            'selected': false,
            'externallySelected': false
          })
        }

        for (let i = 0; i < packagesData.length; i++) {
          self.selectable_packages.push({
            'package': packagesData[i],
            'selected': false,
            'externallySelected': false
          })
        }

        self.fileFlowToPackages = response.data.file_flows_to_packages

        self.setupShowModalArray()
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    setupShowModalArray: function () {
      let self = this

      for (let i = 0; i < self.components.length; i++) {
        self.showModal.push(false)
      }
    },
    fileFlowSelected(fileFlow) {
      // Start by setting all packages to not externally selected
      this.changeAllPackagesExternallySelected(false)

      let fileFlowCode = fileFlow.code
      this.selectedFileFlow = fileFlowCode

      if (_.has(this.fileFlowToPackages, fileFlowCode)) {
        for (let i = 0; i < this.fileFlowToPackages[fileFlowCode].length; i++) {
          let packageCode = this.fileFlowToPackages[fileFlowCode][i].package_code
          this.togglePackageExternallySelected(packageCode)
        }
      }
    },
    togglePackageExternallySelected(packageCode) {
      for (let i = 0; i < this.selectable_packages.length; i++) {
        let currentPackage = this.selectable_packages[i]

        if (currentPackage.package.code === packageCode) {
          currentPackage.externallySelected = !currentPackage.externallySelected
        }
      }
    },
    changeAllPackagesExternallySelected(newStatus) {
      for (let i = 0; i < this.selectable_packages.length; i++) {
        this.selectable_packages[i].externallySelected = newStatus
      }
    },
    packageSelected(selectedPackage) {
      selectedPackage.selected = !selectedPackage.selected
    }
  },
  beforeMount: function () {
    this.loadOrder()
    // this.setupShowModalArray()
  }
}