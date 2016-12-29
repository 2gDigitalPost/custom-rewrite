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

      axios.get('http://localhost:5000/api/v1/orders/', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let ordersData = response.data.orders
        console.log(ordersData)

        for (let i = 0; i < ordersData.length; i++) {
          self.orders.push(ordersData[i])
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadOrders()
  }
}