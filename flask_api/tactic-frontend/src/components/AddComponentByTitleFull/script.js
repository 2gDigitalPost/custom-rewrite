/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'AddComponent',
  components: {
    Multiselect
  },
  data () {
    return {
      titleType: null,
      selectedTitles: [],
      titles: [],
      searchableTitles: [],
      titleNotAvailable: false,
      titleToSearch: null,
      searchResults: [],
      searchResultsAlreadyInTactic: [],
      selectedOMDBTitles: [],
      languages: [],
      selectedLanguages: [],
      selected_pipeline: null,
      pipelines: []
    }
  },
  methods: {
    loadTitles: function () {
      var self = this

      axios.get('/api/v1/titles', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let titleData = response.data.titles

        for (let i = 0; i < titleData.length; i++) {
          self.titles.push({name: titleData[i].name, code: titleData[i].code, type: titleData[i].type})
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadLanguages: function () {
      var self = this
      
      axios.get('/api/v1/languages', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let languageData = response.data.languages

        for (let i = 0; i < languageData.length; i++) {
          self.languages.push({name: languageData[i].name, code: languageData[i].code})
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadPipelines: function () {
      var self = this

      axios.get('/api/v1/pipelines/component', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let pipelineData = response.data.pipelines

        for (let i = 0; i < pipelineData.length; i++) {
          self.pipelines.push(pipelineData[i])
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    searchOMDB: function () {
      let self = this
      self.searchResults = []
      self.searchResultsAlreadyInTactic = []

      let omdbURL = 'http://www.omdbapi.com'

      axios.get(omdbURL, {
        params: {
          s: self.titleToSearch,
          type: self.titleType
        }
      })
      .then(function (response) {
        let gotResponse = response.data.Response

        if (gotResponse) {
          for (let i = 0; i < response.data.Search.length; i++) {
            self.getTitleExistsByIMDbID(response.data.Search[i])
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    getDetailsFromOMDb: function (imdbID) {
      var self = this

      let omdbURL = 'http://www.omdbapi.com'

      axios.get(omdbURL, {
        params: {
          i: imdbID
        }
      })
      .then(function (response) {
        let gotResponse = response.data.Response

        if (gotResponse) {
          return response.data
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    getTitleExistsByIMDbID: function (title) {
      var self = this

      axios.get('/api/v1/titles/imdb/' + title.imdbID + '/exists', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        if (response.data.exists == true) {
          self.searchResultsAlreadyInTactic.push(title)
        }
        else {
          self.searchResults.push(title)
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitOMDbTitlesToTactic: function () {
      let self = this

      if (self.selectedOMDBTitles.length === 0) {
        window.alert("You didn't select any titles!")
      }
      else {
        for (let i = 0; i < self.selectedOMDBTitles.length; i++) {
          let titleObject = self.getDetailsFromOMDb(self.selectedOMDBTitles[i].imdbID)

          console.log(titleObject)
        }
      }
    }
  },
  watch: {
    titleType: function () {
      this.searchableTitles = []

      if (this.titleType === 'Movie') {
        for (let i = 0; i < this.titles.length; i++) {
          if (this.titles[i].type === 'movie') {
            this.searchableTitles.push(this.titles[i])
          }
        }
      } else if (this.titleType === 'Trailer') {
        for (let i = 0; i < this.titles.length; i++) {
          if (this.titles[i].type === 'trailer') {
            this.searchableTitles.push(this.titles[i])
          }
        }
      } else if (this.titleType === 'Episode') {
        for (let i = 0; i < this.titles.length; i++) {
          if (this.titles[i].type === 'episode') {
            this.searchableTitles.push(this.titles[i])
          }
        }
      }
    }
  },
  beforeMount: function () {
    this.loadTitles()
    this.loadLanguages()
    this.loadPipelines()
  }
}