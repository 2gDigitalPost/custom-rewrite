/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import TableSearch from '../TableSearch/index.vue'
import PlatformEntryForm from '../PlatformEntryForm/index.vue'

import bus from '../../bus'

export default {
  name: 'PlatformTable',
  components: {
    TableSearch,
    PlatformEntryForm
  },
  data () {
    return {
      platforms: [],
      displaySearch: false,
      searchColumn: null,
      searchFilter: null,
      showEnterPlatformForm: false
    }
  },
  methods: {
    reloadTable: function () {
      // Reset all the component values to their defaults
      this.platforms = []
      this.displaySearch = false
      this.searchColumn = null
      this.searchFilter = null
      this.showEnterPlatformForm = false

      // Refresh the platforms
      this.loadPlatforms()
    },
    loadPlatforms: function () {
      var self = this

      axios.get('/api/v1/platforms', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.platforms = _.orderBy(response.data.platforms, [platform => platform.name.toLowerCase()])
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openPlatformLink: function(platformCode) {
      let platformDetailURL = '/platform/' + platformCode

      this.$router.push(platformDetailURL)
    },
    setSearchQueryValues: function (searchName, searchValue) {
      this.searchColumn = searchName
      this.searchFilter = searchValue
    }
  },
  computed: {
    searchOptions: function () {
      let options = [{'name': 'code', 'type': 'text'}, {'name': 'name', 'type': 'text'}]

      return options
    },
    platformsToDisplay: function () {
      let platformsList = this.platforms
      let column = this.searchColumn
      let query = this.searchFilter

      if (!_.isEmpty(platformsList) && column && query) {
        if (typeof(query) === 'string') {
          query = query.toLowerCase()

          return _.filter(platformsList, function(platform) {
            return _.includes(platform[column].toLowerCase(), query)
          })
        }
        else if (Array.isArray(query)) {
          if (query.length > 0) {
            return _.filter(platformsList, function(platform) {
              return _.includes(query, platform[column])
            })
          }
        }
      }
      
      return this.platforms
    }
  },
  beforeMount: function () {
    this.loadPlatforms()
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