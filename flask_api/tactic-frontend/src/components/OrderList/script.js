/* globals localStorage */

import axios from 'axios'

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

        for (let i = 0; i < ordersData.length; i++) {
          self.orders.push(ordersData[i])
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openOrderLink: function(orderCode) {
      let orderDetailURL = '/orders/' + orderCode

      this.$router.push(orderDetailURL)
    }
  },
  beforeMount: function () {
    this.loadOrders()
  }
}