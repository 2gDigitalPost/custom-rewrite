/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'
import SelectableComponent from './SelectableComponent/index.vue'

export default {
  name: 'SelectPipelines',
  components: {
    Multiselect,
    'selectable-component': SelectableComponent,
  },
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      components: [],
      packages: [],
      selected_pipeline: null,
      pipelines: [],
      pipelines_dict: {},
      checkedComponents: []
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
        self.components = componentsData
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadPipelines: function () {
      var self = this

      axios.get('/api/v1/pipelines/component', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let pipelineData = response.data.pipelines

        for (let i = 0; i < pipelineData.length; i++) {
          self.pipelines.push(pipelineData[i])

          self.pipelines_dict[pipelineData[i].code] = pipelineData[i]
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    getFullPipelineFromCode: function (pipelineCode) {
      var self = this

      return this.pipelines_dict[pipelineCode]
    }
  },
  beforeMount: function () {
    this.loadOrder()
    this.loadPipelines()
  }
}