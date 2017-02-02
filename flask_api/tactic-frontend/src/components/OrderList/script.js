/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'OrderList',
  data () {
    return {
      orders: []
    }
  },
  methods: {
    loadOrders: function () {
      var self = this

      axios.get('/api/v1/orders', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let ordersData = response.data.orders

        self.orders = self.sortByDueDate(response.data.orders)
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openOrderLink: function(orderCode) {
      let orderDetailURL = '/orders/' + orderCode

      this.$router.push(orderDetailURL)
    },
    loadOrderEntryLink: function() {
      this.$router.push('/orders/new')
    },
    sortByDueDate: function (orderObjects) {
      return _.sortBy(orderObjects, 'due_date')
    }
  },
  beforeMount: function () {
    this.loadOrders()
  }
}