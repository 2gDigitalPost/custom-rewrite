/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import moment from 'moment'

import TableSearch from '../TableSearch/index.vue'

import bus from '../../bus'

export default {
  name: 'OrderList',
  components: {
    TableSearch
  },
  data () {
    return {
      orders: [],
      searchColumn: null,
      searchFilter: null
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
    },
    getTitleListForOrder: function (order) {
      let titles = order['title_sobjects']

      if (_.isEmpty(titles)) return "None"

      let titlesToDisplay = _.take(titles, 3)
      let titlesString = _.join(_.map(titlesToDisplay, 'name'), ', ')

      if (titles.length > 3) {
        titlesString += ', + ' + (titles.length - 3) + ' more' 
      }

      return titlesString
    },
    getLoginName: function(login) {
      return _.startCase(_.toLower(login))
    },
    dateFormatted: function (date) {
      return moment(date).format('ddd, MMM Do YYYY, h:mm A')
    },
    setSearchQueryValues: function (searchName, searchValue) {
      this.searchColumn = searchName
      this.searchFilter = searchValue
    }
  },
  beforeMount: function () {
    this.loadOrders()
  },
  computed: {
    searchOptions: function () {
      let options = [{'name': 'code', 'type': 'text'}]

      let divisions = _.uniqBy(_.map(this.orders, 'division'), 'code')
      let divisionOptions = []

      _.forEach(divisions, function(division) {
        divisionOptions.push({'label': division['name'], 'value': division['code']})
      })

      options.push({'name': 'division_code', 'type': 'select', 'options': divisionOptions, 'label': 'Division'})

      return options
    },
    ordersToDisplay: function () {
      let orderList = this.orders
      let column = this.searchColumn
      let query = this.searchFilter

      if (!_.isEmpty(orderList) && column && query) {
        if (typeof(query) === 'string') {
          query = query.toLowerCase()

          return _.filter(orderList, function(order) {
            return _.includes(order[column].toLowerCase(), query)
          })
        }
        else if (Array.isArray(query)) {
          if (query.length > 0) {
            return _.filter(orderList, function(order) {
              return _.includes(query, order[column])
            })
          }
        }
      }
      
      return this.orders
    }
  },
  created() {
    bus.$on('search-query', this.setSearchQueryValues)
  },
  destroyed() {
    bus.$off('search-query', this.setSearchQueryValues)
  }
}