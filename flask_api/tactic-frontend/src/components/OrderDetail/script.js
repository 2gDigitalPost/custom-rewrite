/* globals localStorage */

import axios from 'axios'

export default {
  name: 'OrderDetail',
  data () {
    return {
      order_code: this.$route.params.code,
      order_sobject: null,
      order_name: null,
      components: [],
      packages: [],
      add_title_link: null
    }
  },
  methods: {
    loadOrder: function () {
      var self = this

      axios.get('http://localhost:5000/api/v1/orders/' + self.order_code + '/full', {
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
        self.add_title_link = '/orders/' + self.order_code + '/titles/add'

        console.log(orderData)
        console.log(self.order_sobject)
        console.log(componentsData)
        console.log(packagesData)
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadOrder()
  }
}