import axios from 'axios'
import _ from 'lodash'

import bus from '../../bus'

export default {
  name: 'PurchaseOrderEntryForm',
  props: ['division'],
  data () {
    return {
      number: null,
      searching: false,
      puchaseOrderExists: false,
      inputError: false,
      inputOkay: false
    }
  },
  methods: {
    getExistingPurchaseOrder: _.debounce(
      function () {
        let self = this

        if (self.number === null || self.number === '') return

        self.searching = true

        axios.get('/api/v1/purchase-order/number/' + self.number + '/division/' + self.division + '/exists', {
          params: {
            token: localStorage.tactic_token
          }
        })
        .then(function (response) {
          if (response.data.result_found) {
            self.purchaseOrderExists = true
            self.inputError = true
            self.inputOkay = false
          }
          else {
            self.purchaseOrderExists = false
            self.inputError = false
            self.inputOkay = true
          }

          self.searching = false
          bus.$emit('po-number-changed', self.number, self.purchaseOrderExists)
        })
        .catch(function (error) {
          console.log(error)
        })
      }, 500
    )
  },
  watch: {
    number: function () {
      this.getExistingPurchaseOrder()
    },
    division: function () {
      this.getExistingPurchaseOrder()
    }
  }
}