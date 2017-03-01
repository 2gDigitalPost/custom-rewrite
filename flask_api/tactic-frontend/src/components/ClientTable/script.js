/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import TableSearch from '../TableSearch/index.vue'
import ClientEntryForm from '../ClientEntryForm/index.vue'

import bus from '../../bus'

export default {
  name: 'ClientTable',
  components: {
    TableSearch,
    ClientEntryForm
  },
  data () {
    return {
      clients: [],
      displaySearch: false,
      searchColumn: null,
      searchFilter: null,
      showAddForm: false,
      currentPage: 1,
      numberOfResultsDisplayed: 50
    }
  },
 methods: {
    reloadTable: function () {
      // Reset all the component values to their defaults
      this.clients = []
      this.displaySearch = false
      this.searchColumn = null
      this.searchFilter = null
      this.showAddForm = false

      // Refresh the platforms
      this.loadClients()
    },
    loadClients: function () {
      var self = this

      axios.get('/api/v1/clients', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.clients = response.data.clients
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openObjectLink: function(code) {
      let redirectURL = '/client/' + code

      this.$router.push(redirectURL)
    },
    setSearchQueryValues: function (searchName, searchValue) {
      this.searchColumn = searchName
      this.searchFilter = searchValue
    },
    modifyCurrentPage: function (modifier) {
      this.currentPage += modifier
    }
  },
  computed: {
    searchOptions: function () {
      let options = [{'name': 'code', 'type': 'text'}, {'name': 'name', 'type': 'text'}]

      return options
    },
    objectsToDisplay: function () {
      let clientList = this.clients
      let column = this.searchColumn
      let query = this.searchFilter
      let numberOfResults = this.numberOfResultsDisplayed
      let page = this.currentPage - 1

      let chunkedObjects = []

      if (!_.isEmpty(clientList) && column && query) {
        if (typeof(query) === 'string') {
          query = query.toLowerCase()

          chunkedObjects = _.chunk(_.filter(clientList, function(client) {
            return _.includes(client[column].toLowerCase(), query)
          }), numberOfResults)
        }
        else if (Array.isArray(query)) {
          if (query.length > 0) {
             chunkedObjects = _.chunk(_.filter(clientList, function(client) {
               return _.includes(query, client[column])
            }), numberOfResults)
          }
        }
      }
      else {
        chunkedObjects = _.chunk(clientList, numberOfResults)
      }
      
      return chunkedObjects[page]
    },
    numberOfPages: function () {
      return Math.ceil(this.clients.length / this.numberOfResultsDisplayed)
    }
  },
  beforeMount: function () {
    this.loadClients()
  },
  created() {
    bus.$on('search-query', this.setSearchQueryValues)
    bus.$on('reload-page', this.reloadTable)
  },
  destroyed() {
    bus.$off('search-query', this.setSearchQueryValues)
    bus.$off('reload-page', this.reloadTable)
  }
}