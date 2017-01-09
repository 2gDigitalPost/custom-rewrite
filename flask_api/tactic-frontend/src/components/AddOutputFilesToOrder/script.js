/* globals localStorage */

import axios from 'axios'
import ComponentWithOutputFiles from './ComponentWithOutputFiles/index.vue'
import FileFlowSelectable from './FileFlowSelectable/index.vue'
import PackageSelectable from './PackageSelectable/index.vue'

import bus from '../../bus'

export default {
  name: 'AddOutputFilesToOrder',
  components: {
    'component-with-output-files': ComponentWithOutputFiles,
    'file-flow-selectable': FileFlowSelectable,
    'package-selectable': PackageSelectable
  },
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      selectable_components: [],
      selectable_packages: [],
      changes: [],
      file_name: null,
      file_type: null,
      fileFlows: [],
      fileFlowToComponents: [],
      fileFlowToPackages: [],
      selectedFileFlow: null
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
        let componentsData = response.data.components
        let packagesData = response.data.packages

        self.order_sobject = orderData
        self.order_name = orderData['name']

        for (let i = 0; i < componentsData.length; i++) {
          self.selectable_components.push({
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
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadFileFlows: function () {
      var self = this

      axios.get('/api/v1/orders/' + self.order_code + '/file-flows', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let fileFlowData = response.data.file_flows
        let fileFlowToComponentData = response.data.file_flow_to_components
        let fileFlowToPackageData = response.data.file_flow_to_packages

        self.fileFlows = fileFlowData
        self.fileFlowToComponents = fileFlowToComponentData
        self.fileFlowToPackages = fileFlowToPackageData
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    fileFlowSelected: function (fileFlowCode, selected) {
      let self = this
    
      for (let i = 0; i < self.fileFlows.length; i++) {
        if (self.fileFlows[i].code === fileFlowCode) {
          self.selectedFileFlow = self.fileFlows[i]

          break
        }
      }

      for (let i = 0; i < self.fileFlowToComponents.length; i++) {
        if (self.fileFlowToComponents[i].file_flow_code === fileFlowCode) {
          let componentCode = self.fileFlowToComponents[i].component_code

          for (let j = 0; j < self.selectable_components.length; j++) {
            if (self.selectable_components[j].component.code === componentCode) {
              self.selectable_components[j].externallySelected = selected
            }
          }
        }
      }

      for (let i = 0; i < self.fileFlowToPackages.length; i++) {
        if (self.fileFlowToPackages[i].file_flow_code === fileFlowCode) {
          let packageCode = self.fileFlowToPackages[i].package_code

          for (let j = 0; j < self.selectable_packages.length; j++) {
            if (self.selectable_packages[j].package.code === packageCode) {
              self.selectable_packages[j].externallySelected = selected
            }
          }
        }
      }
      
      self.updateChangeArray()
    },
    componentSelected: function (componentCode) {
      var self = this

      for (let i = 0; i < self.selectable_components.length; i++) {
        if (self.selectable_components[i].component.code === componentCode) {
          self.selectable_components[i].selected = !self.selectable_components[i].selected
        }
      }
    },
    packageSelected: function (packageCode) {
      var self = this

      for (let i = 0; i < self.selectable_packages.length; i++) {
        if (self.selectable_packages[i].package.code === packageCode) {
          self.selectable_packages[i].selected = !self.selectable_packages[i].selected
        }
      }
    },
    updateChangeArray: function () {
      var self = this

      self.changes = []

      if (self.selectedFileFlow !== null) {
        for (let i = 0; i < self.selectable_components.length; i++) {
          let selectedComponent = self.selectable_components[i]

          if (selectedComponent.selected && selectedComponent.externallySelected) {
            self.changes.push("The link between " + selectedComponent.component.name + " (" + selectedComponent.component.code + ") and " + self.selectedFileFlow.name + " (" + self.selectedFileFlow.code + ") will be removed")
          }
          else if (selectedComponent.selected) {
            self.changes.push("A link between " + selectedComponent.component.name + " (" + selectedComponent.component.code + ") and " + self.selectedFileFlow.name + " (" + self.selectedFileFlow.code + ") will be added")
          }
        }

        for (let i = 0; i < self.selectable_packages.length; i++) {
          let selectedPackage = self.selectable_packages[i]

          if (selectedPackage.selected && selectedPackage.externallySelected) {
            self.changes.push("The link between " + selectedPackage.package.name + " (" + selectedPackage.package.code + ") and " + self.selectedFileFlow.name + " (" + self.selectedFileFlow.code + ") will be removed")
          }
          else if (selectedPackage.selected) {
            self.changes.push("A link between " + selectedPackage.package.name + " (" + selectedPackage.package.code + ") and " + self.selectedFileFlow.name + " (" + self.selectedFileFlow.code + ") will be added")
          }
        }
      }
    }
  },
  beforeMount: function () {
    this.loadOrder()
    this.loadFileFlows()
  },
  watch: {
    selectable_components: {
      handler: function (val, oldVal) {
        this.updateChangeArray()
      },
      deep: true
    },
    selectable_packages: {
      handler: function (val, oldVal) {
        this.updateChangeArray()
      },
      deep: true
    },
  },
  created() {
    bus.$on('file-flow-selected', this.fileFlowSelected)
    bus.$on('component-selected', this.componentSelected)
    bus.$on('package-selected', this.packageSelected)
  },
  destroyed() {
    bus.$off('file-flow-selected', this.fileFlowSelected)
    bus.$on('component-selected', this.componentSelected)
    bus.$on('package-selected', this.packageSelected)
  }
}