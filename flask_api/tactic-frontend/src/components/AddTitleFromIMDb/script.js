/* globals localStorage */

import axios from 'axios'

export default {
  name: 'AddTitleFromIMDb',
  data () {
    return {
      title_search_name: null,
      title_type: null,
      search_results: [],
      selected_title: null,
      selected_title_full: null
    }
  },
  methods: {
    searchOMDb: function () {
      this.searchOMDbForMovie()
    },
    searchOMDbForMovie: function () {
      var self = this
      self.search_results = []
      let omdbURL = 'http://www.omdbapi.com'

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
    },
    getDetailsFromOMDb: function () {
      var self = this

      let omdbURL = 'http://www.omdbapi.com'

      axios.get(omdbURL, {
        params: {
          i: self.selected_title.imdbID
        }
      })
      .then(function (response) {
        let gotResponse = response.data.Response

        if (gotResponse) {
          console.log(response.data)

          let searchResults = response.data

          self.selected_title_full = searchResults
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    addTitleToTactic: function () {
      var self = this

      axios.post('/api/v1/titles', 
        JSON.stringify({
          'actors': self.selected_title_full.Actors,
          'awards': self.selected_title_full.Awards,
          'country': self.selected_title_full.Country,
          'director': self.selected_title_full.Director,
          'genre': self.selected_title_full.Genre,
          'language': self.selected_title_full.Language,
          'metascore': parseInt(self.selected_title_full.Metascore),
          'plot': self.selected_title_full.Plot,
          'poster': self.selected_title_full.Poster,
          'rated': self.selected_title_full.Rated,
          'released': self.selected_title_full.Released,
          'runtime': self.selected_title_full.Runtime,
          'name': self.selected_title_full.Title,
          'writer': self.selected_title_full.Writer,
          'year': self.selected_title_full.Year,
          'imdb_id': self.selected_title_full.imdbID,
          'imdb_rating': parseFloat(self.selected_title_full.imdbRating.replace(/,/g, '')),
          'imdb_votes': parseInt(self.selected_title_full.imdbVotes),
          'type': self.title_type.toLowerCase(),
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            self.$router.go(self.$router.currentRoute)
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  watch: {
    selected_title: function () {
      this.getDetailsFromOMDb()
    }
  }
}