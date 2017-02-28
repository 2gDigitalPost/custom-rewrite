/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import TableSearch from '../TableSearch/index.vue'
import ElementEvaluationEntryForm from '../ElementEvaluationEntryForm/index.vue'

import bus from '../../bus'

export default {
  name: 'ElementEvaluationTable',
  components: {
    TableSearch,
    ElementEvaluationEntryForm
  },
  data () {
    return {
      elementEvaluations: [],
      displaySearch: false,
      searchColumn: null,
      searchFilter: null,
      showEnterElementEvaluationForm: false
    }
  },
  methods: {
    reloadTable: function () {
      // Reset all the component values to their defaults
      this.elementEvaluations = []
      this.displaySearch = false
      this.searchColumn = null
      this.searchFilter = null
      this.showEnterElementEvaluationForm = false

      // Refresh the platforms
      this.loadElementEvaluations()
    },
    loadElementEvaluations: function () {
      var self = this

      axios.get('/api/v1/element-evaluations', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.elementEvaluations = response.data.element_evaluations
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    openElementEvaluationLink: function(elementEvaluationCode) {
      let elementEvaluationDetailURL = '/element-evaluation/' + elementEvaluationCode

      this.$router.push(elementEvaluationDetailURL)
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
    elementEvaluationsToDisplay: function () {
      let elementEvaluationsList = this.elementEvaluations
      let column = this.searchColumn
      let query = this.searchFilter

      if (!_.isEmpty(elementEvaluationsList) && column && query) {
        if (typeof(query) === 'string') {
          query = query.toLowerCase()

          return _.filter(elementEvaluationsList, function(elementEvaluation) {
            return _.includes(elementEvaluation[column].toLowerCase(), query)
          })
        }
        else if (Array.isArray(query)) {
          if (query.length > 0) {
            return _.filter(elementEvaluationsList, function(elementEvaluation) {
              return _.includes(query, elementEvaluation[column])
            })
          }
        }
      }
      
      return this.elementEvaluations
    }
  },
  beforeMount: function () {
    this.loadElementEvaluations()
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