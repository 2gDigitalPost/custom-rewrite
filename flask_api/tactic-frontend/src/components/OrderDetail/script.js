/* globals localStorage */

import axios from 'axios'

import ComponentEditableList from './ComponentEditableList/index.vue'
import PackageEditableList from './PackageEditableList/index.vue'
import FileEditableList from './FileEditableList/index.vue'

import bus from '../../bus'

export default {
  name: 'OrderDetail',
  components: {
    ComponentEditableList,
    PackageEditableList,
    FileEditableList
  },
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      division: null,
      divisionImage: null,
      components: [],
      componentsFull: [],
      packages: [],
      add_title_link: null,
      edit_components_link: null,
      add_output_files_link: null,
      files: []
    }
  },
  methods: {
    loadOrder: function () {
      var self = this

      self.order_sobject = null
      self.order_name = null
      self.division = null
      self.divisionImage = null
      self.components = []
      self.componentsFull = []
      self.packages = []
      self.files = []

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
        self.division = response.data.division
        self.divisionImage = response.data.division_image
        self.components = componentsData
        self.componentsFull = response.data.components_full
        self.packages = packagesData
        self.files = response.data.files
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
  computed: {
    divisionImageSource: function () {
      if (this.divisionImage !== null) {
        return 'http://localhost:8081/assets/twog/division/' + this.divisionImage
      }
    }
  },
  created() {
    bus.$on('component-title-updated', this.loadOrder)
    bus.$on('task-updated', this.loadOrder)
    bus.$on('new-file-added-to-order', this.loadOrder)
    bus.$on('file-updated', this.loadOrder)
  },
  destroyed() {
    bus.$off('component-title-updated', this.loadOrder)
    bus.$off('task-updated', this.loadOrder)
    bus.$off('new-file-added-to-order', this.loadOrder)
    bus.$off('file-updated', this.loadOrder)
  }
}