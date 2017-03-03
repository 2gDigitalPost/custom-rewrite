/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import moment from 'moment'

import TableSearch from '../TableSearch/index.vue'
import ProjectTemplateRequest from '../ProjectTemplateRequest/index.vue'

import bus from '../../bus'

export default {
  name: 'ProjectTemplateRequestTable',
  components: {
    TableSearch,
    ProjectTemplateRequest
  },
  data () {
    return {
      projectTemplateRequests: [],
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
      this.projectTemplateRequests = []
      this.displaySearch = false
      this.searchColumn = null
      this.searchFilter = null
      this.showAddForm = false

      // Refresh the platforms
      this.loadProjectTemplateRequests()
    },
    loadProjectTemplateRequests: function () {
      var self = this

      axios.get('/api/v1/project-templates/requests', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.projectTemplateRequests = response.data.project_template_requests
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openObjectLink: function(code) {
      let redirectURL = '/project-templates/requests/' + code

      this.$router.push(redirectURL)
    },
    setSearchQueryValues: function (searchName, searchValue) {
      this.searchColumn = searchName
      this.searchFilter = searchValue
    },
    modifyCurrentPage: function (modifier) {
      this.currentPage += modifier
    },
    getLoginName: function(login) {
      return _.startCase(_.toLower(login))
    },
    dateFormatted: function (date) {
      return moment(date).format('ddd, MMM Do YYYY, h:mm A')
    },
  },
  computed: {
    searchOptions: function () {
      let options = [{'name': 'code', 'type': 'text'}, {'name': 'name', 'type': 'text'}]

      return options
    },
    objectsToDisplay: function () {
      let objectList = this.projectTemplateRequests
      let column = this.searchColumn
      let query = this.searchFilter
      let numberOfResults = this.numberOfResultsDisplayed
      let page = this.currentPage - 1

      let chunkedObjects = []

      if (!_.isEmpty(objectList) && column && query) {
        if (typeof(query) === 'string') {
          query = query.toLowerCase()

          chunkedObjects = _.chunk(_.filter(objectList, function(object) {
            return _.includes(object[column].toLowerCase(), query)
          }), numberOfResults)
        }
        else if (Array.isArray(query)) {
          if (query.length > 0) {
             chunkedObjects = _.chunk(_.filter(objectList, function(object) {
               return _.includes(query, object[column])
            }), numberOfResults)
          }
        }
      }
      else {
        chunkedObjects = _.chunk(objectList, numberOfResults)
      }
      
      return chunkedObjects[page]
    },
    numberOfPages: function () {
      return Math.ceil(this.projectTemplateRequests.length / this.numberOfResultsDisplayed)
    }
  },
  beforeMount: function () {
    this.loadProjectTemplateRequests()
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