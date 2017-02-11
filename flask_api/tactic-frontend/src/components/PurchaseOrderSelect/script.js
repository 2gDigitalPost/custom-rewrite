/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../bus'

export default {
  name: 'PurchaseOrderSelect',
  props: ['division'],
  components: {
    Multiselect
  },
  data () {
    return {
      loading: true,
      purchaseOrderOptions: [],
      selectedPurchaseOrder: null,
    }
  },
  methods: {
    loadPurchaseOrders: function () {
      var self = this

      self.loading = true

      axios.get('/api/v1/division/' + self.division + '/purchase-orders', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        console.log(response)
        let purchaseOrderData = response.data.purchase_orders

        for (let i = 0; i < purchaseOrderData.length; i++) {
          self.purchaseOrderOptions.push({code: purchaseOrderData[i].code, number: purchaseOrderData[i].name})
        }

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
  },
  watch: {
    selectedPurchaseOrder: function () {
      let purchaseOrderCode = null

      if (this.selectedPurchaseOrder) {
        purchaseOrderCode = this.selectedPurchaseOrder.code
      }

      bus.$emit('purchase-order-selected', purchaseOrderCode)
    }
  },
  beforeMount: function () {
    this.loadPurchaseOrders()
  }
}