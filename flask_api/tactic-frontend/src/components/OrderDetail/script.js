/* globals localStorage */

import axios from 'axios'

import ComponentEditableList from './ComponentEditableList/index.vue'
import PackageDetailList from '../PackageDetailList/index.vue'

import bus from '../../bus'

export default {
  name: 'OrderDetail',
  components: {
    ComponentEditableList,
    'package-detail-list': PackageDetailList
  },
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      components: [],
      componentsFull: [],
      packages: [],
      add_title_link: null,
      edit_components_link: null,
      add_output_files_link: null
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
        self.componentsFull = response.data.components_full
        self.packages = packagesData
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    setupLinks: function () {
      this.add_title_link = '/orders/' + this.order_code + '/titles/add'
      this.edit_components_link = '/orders/' + this.order_code + '/components'
      this.add_output_files_link = '/orders/' + this.order_code + '/file-flows/add'
    }
  },
  beforeMount: function () {
    this.loadOrder()
    this.setupLinks()
  },
  created() {
    bus.$on('component-title-updated', this.loadOrder)
  },
  destroyed() {
    bus.$off('component-title-updated', this.loadOrder)
  }
}