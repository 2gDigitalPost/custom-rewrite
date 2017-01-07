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
      file_name: null,
      file_type: null,
      fileFlows: [],
      fileFlowToComponents: [],
      fileFlowToPackages: []
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
            'selected': false
          })
        }

        for (let i = 0; i < packagesData.length; i++) {
          self.selectable_packages.push({
            'package': packagesData[i],
            'selected': false
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

      let componentCodes = []

      for (let i = 0; i < self.fileFlowToComponents.length; i++) {
        if (self.fileFlowToComponents[i].file_flow_code === fileFlowCode) {
          let componentCode = self.fileFlowToComponents[i].component_code

          for (let j = 0; j < self.selectable_components.length; j++) {
            if (self.selectable_components[j].component.code === componentCode) {
              componentCodes.push(componentCode)
            }
          }
        }
      }

      let packageCodes = []

      for (let i = 0; i < self.fileFlowToPackages.length; i++) {
        if (self.fileFlowToPackages[i].file_flow_code === fileFlowCode) {
          let packageCode = self.fileFlowToPackages[i].package_code

          for (let j = 0; j < self.selectable_packages.length; j++) {
            if (self.selectable_packages[j].package.code === packageCode) {
              packageCodes.push(packageCode)
            }
          }
        }
      }
      
      bus.$emit('highlight-components', componentCodes, selected)
      bus.$emit('highlight-packages', packageCodes, selected)
    }
  },
  beforeMount: function () {
    this.loadOrder()
    this.loadFileFlows()
  },
  created() {
    bus.$on('file-flow-selected', this.fileFlowSelected)
  },
  destroyed() {
    bus.$off('file-flow-selected', this.fileFlowSelected)
  }
}