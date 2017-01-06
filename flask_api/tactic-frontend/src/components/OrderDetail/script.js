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
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    setupLinks: function () {
      this.add_title_link = '/orders/' + this.order_code + '/titles/add'
      this.edit_components_link = '/orders/' + this.order_code + '/components'
      this.add_output_files_link = '/orders/' + this.order_code + '/output-files/add'
    }
  },
  beforeMount: function () {
    this.loadOrder()
    this.setupLinks()
  }
}