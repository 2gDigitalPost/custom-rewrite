/* globals localStorage */

import axios from 'axios'

export default {
  name: 'AddTitleFromIMDb',
  data () {
    return {
      title_search_name: null,
      title_type: null,
      search_results: []
    }
  },
  methods: {
    searchOMDb: function () {
      this.searchOMDbForMovie()
    },
    searchOMDbForMovie: function () {
      var self = this
      self.search_results = []
      let omdbURL = 'http:///www.omdbapi.com'

      axios.get(omdbURL, {
        params: {
          s: self.title_search_name,
          type: self.title_type
        }
      })
      .then(function (response) {
        console.log(response)
        let gotResponse = response.data.Response

        if (gotResponse) {
          let searchResults = response.data.Search

          for (let i = 0; i < searchResults.length; i++) {
            self.search_results.push(searchResults[i])
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}