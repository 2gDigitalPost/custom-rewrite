/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'AddComponentByTitleFull',
  components: {
    Multiselect
  },
  data () {
    return {
      loading: true,
      titleType: null,
      selectedTitles: [],
      titles: [],
      titleNotAvailable: false,
      titleToSearch: null,
      omdbSearched: false,
      searchResults: [],
      totalSearchResults: null,
      currentPage: null,
      totalPages: null,
      searchResultsAlreadyInTactic: [],
      selectedOMDBTitles: [],
      titleNotInOMDb: false,
      languages: [],
      selectedLanguages: [],
      selectedProjectTemplate: null,
      projectTemplates: [],
      splitInstructions: false,
      submitting: false,
      newComponentsSubmitted: false,
      newTitleName: null,
      year: null,
      yearOptions: this.getYearOptions()
    }
  },
  methods: {
    loadTitles: function () {
      var self = this

      self.loading = true

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

        self.loading = false
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
    loadProjectTemplates: function () {
      var self = this

      axios.get('/api/v1/project-templates', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        let projectTemplateData = response.data.project_templates

        for (let i = 0; i < projectTemplateData.length; i++) {
          self.projectTemplates.push({name: projectTemplateData[i].name, code: projectTemplateData[i].code})
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    reloadAll: function () {
      // Reset all variables to their defaults
      this.loading = true
      this.titleType = null
      this.selectedTitles = []
      this.titles = []
      this.titleNotAvailable = false
      this.titleToSearch = null
      this.omdbSearched = false
      this.searchResults = []
      this.totalSearchResults = null
      this.currentPage = null
      this.totalPages = null
      this.searchResultsAlreadyInTactic = []
      this.selectedOMDBTitles = []
      this.titleNotInOMDb = false
      this.languages = []
      this.selectedLanguages = []
      this.selectedProjectTemplate = null
      this.projectTemplates = []
      this.splitInstructions = false
      this.submitting = false
      this.newComponentsSubmitted = false
      this.newTitleName
      this.year = null

      this.loadTitles()
      this.loadLanguages()
      this.loadProjectTemplates()
    },
    redirectToOrderDetail: function () {
      this.$router.push('/orders/' + this.$route.params.code)
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

        self.omdbSearched = true

        if (gotResponse) {
          for (let i = 0; i < response.data.Search.length; i++) {
            self.getTitleExistsByIMDbID(response.data.Search[i])
          }

          self.totalSearchResults = response.data.totalResults
          self.currentPage = 1
          self.totalPages = Math.ceil(self.totalSearchResults / 10)
        }
      })
      .catch(function (error) {
        console.log(error)

        if (error.response) {
          if (error.response.status === 503) {
            window.alert("The OMDb API is returning status 503. This means the service is currently unavailable. Please try again later, or enter the Title manually.")
          }
        }
      })
    },
    searchOMDBWithPageNumber: function (pageNumber) {
      let self = this
      self.searchResults = []
      self.searchResultsAlreadyInTactic = []

      let omdbURL = 'http://www.omdbapi.com'

      axios.get(omdbURL, {
        params: {
          s: self.titleToSearch,
          type: self.titleType,
          page: pageNumber
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
    previousPage: function () {
      let self = this

      if (self.currentPage > 1) {
        self.currentPage--
      }

      self.searchOMDBWithPageNumber(self.currentPage)
    },
    nextPage: function () {
      let self = this

      if (self.currentPage < self.totalPages) {
        self.currentPage++
      }

      self.searchOMDBWithPageNumber(self.currentPage)
    },
    getDetailsFromOMDb: function (imdbID) {
      var self = this

      let omdbURL = 'http://www.omdbapi.com?i=' + imdbID

      return axios.get(omdbURL)
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
          let titleObject = self.getDetailsFromOMDb(self.selectedOMDBTitles[i])

          titleObject.then(function (responseData) {
            let titleData = responseData.data

            let jsonToSend = {
              'title_data': {
                'actors': titleData.Actors,
                'awards': titleData.Awards,
                'country': titleData.Country,
                'director': titleData.Director,
                'genre': titleData.Genre,
                'language': titleData.Language,
                'metascore': parseInt(titleData.Metascore),
                'plot': titleData.Plot,
                'poster': titleData.Poster,
                'rated': titleData.Rated,
                'released': titleData.Released,
                'runtime': titleData.Runtime,
                'name': titleData.Title,
                'writer': titleData.Writer,
                'year': titleData.Year,
                'imdb_id': titleData.imdbID,
                'imdb_rating': parseFloat(titleData.imdbRating.replace(/,/g, '')),
                'imdb_votes': parseInt(titleData.imdbVotes),
                'type': titleData.Type
              },
              'token': localStorage.tactic_token
            }

            axios.post('/api/v1/titles/omdb', JSON.stringify(jsonToSend), {
              headers: {
                'Content-Type': 'application/json;charset=UTF-8'
              },
            })
            .then(function (response) {
              if (response.status === 200) {
                self.reloadAll()
              }
            })
            .catch(function (error) {
              console.log(error)
            })
          })
          .catch(function (error) {
            console.log(error)
          })
        }
      }
    },
    submitNewComponentsToTactic: function () {
      var self = this

      self.submitting = true

      let orderCode = self.$route.params.code

      let apiURL = '/api/v1/orders/' + orderCode + '/create-from-template'
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'titles': self.selectedTitles,
        'languages': self.selectedLanguages,
        'project_template_code': self.selectedProjectTemplate.code,
        'split_instructions': self.splitInstructions
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.data) {
          if (response.status === 200) {
            self.submitting = false
            self.newComponentsSubmitted = true
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitManualTitle: function () {
      var self = this

      let jsonToSend = {
        'token': localStorage.tactic_token,
        'title': {
          'name': self.newTitleName,
          'type': self.titleType.toLowerCase(),
        }
      }

      if (self.year !== null) {
        jsonToSend['title']['year'] = self.year
      }

      axios.post('/api/v1/titles/manual', JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data) {
          if (response.status === 200) {
            self.reloadAll()
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    getYearOptions: function () {
      let currentYear = new Date().getFullYear();
      let years = [];

      for (let yearIterator = currentYear; yearIterator >= 1888; yearIterator--) {
        years.push(yearIterator);
      }

      return years;
    }
  },
  computed: {
    searchableTitles: function () {
      let self = this
      let titlesMatchingType = []
      let type = _.lowerCase(self.titleType)

      _.each(self.titles, function (title) {
        if (title.type === type) {
          titlesMatchingType.push(title)
        }
      })

      return _.sortBy(titlesMatchingType, 'name')
    }
  },
  beforeMount: function () {
    this.loadTitles()
    this.loadLanguages()
    this.loadProjectTemplates()
  }
}