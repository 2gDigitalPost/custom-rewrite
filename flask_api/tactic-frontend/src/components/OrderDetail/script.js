/* globals localStorage */

import axios from 'axios'

import ComponentEditableList from './ComponentEditableList/index.vue'
import PackageEditableList from './PackageEditableList/index.vue'
import FileEditableList from './FileEditableList/index.vue'
import EditExpectedCompletionDate from './EditExpectedCompletionDate/index.vue'
import EditDueDate from './EditDueDate/index.vue'

import bus from '../../bus'

export default {
  name: 'OrderDetail',
  components: {
    ComponentEditableList,
    PackageEditableList,
    FileEditableList,
    EditExpectedCompletionDate,
    EditDueDate
  },
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      division: null,
      divisionImage: null,
      editingExpectedCompletionDate: false,
      editingDueDate: false,
      components: [],
      componentsFull: [],
      packages: [],
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
      self.editingExpectedCompletionDate = false
      self.editingDueDate = false
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
    cancelExpectedCompletionDateEdit: function () {
      this.editingExpectedCompletionDate = false
    },
    cancelDueDateEdit: function () {
      this.editingDueDate = false
    }
  },
  beforeMount: function () {
    this.loadOrder()
  },
  computed: {
    addTemplateLink: function () {
      if (this.order_code) {
        return '/orders/' + this.order_code + '/titles/add'
      }
    },
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
    bus.$on('files-imported', this.loadOrder)
    bus.$on('file-removed-from-order', this.loadOrder)
    bus.$on('order-updated', this.loadOrder)
    bus.$on('expected-completion-date-edit-cancel', this.cancelExpectedCompletionDateEdit)
    bus.$on('due-date-edit-cancel', this.cancelDueDateEdit)
    bus.$on('file-flow-updated', this.loadOrder)
  },
  destroyed() {
    bus.$off('component-title-updated', this.loadOrder)
    bus.$off('task-updated', this.loadOrder)
    bus.$off('new-file-added-to-order', this.loadOrder)
    bus.$off('file-updated', this.loadOrder)
    bus.$off('files-imported', this.loadOrder)
    bus.$off('file-removed-from-order', this.loadOrder)
    bus.$off('order-updated', this.loadOrder)
    bus.$off('expected-completion-date-edit-cancel', this.cancelExpectedCompletionDateEdit)
    bus.$off('due-date-edit-cancel', this.cancelDueDateEdit)
    bus.$off('file-flow-updated', this.loadOrder)
  }
}