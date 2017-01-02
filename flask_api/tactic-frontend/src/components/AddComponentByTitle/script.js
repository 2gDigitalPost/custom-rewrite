/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

export default {
  name: 'AddComponent',
  components: {
    Multiselect
  },
  data () {
    return {
      title_type: null,
      selected_title: null,
      selected_language: null,
      selected_languages: [],
      titles: [],
      searchable_titles: [],
      languages: [],
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
    updateSelectedTitle: function (newSelectedTitle) {
      this.selected_title = newSelectedTitle
    },
    updateSelectedLanguages: function (newSelectedLanguage) {
      this.selected_language = newSelectedLanguage
    }
  },
  beforeMount: function () {
    this.loadTitles()
    this.loadLanguages()
  },
  computed: {
    created_components: function() {
      if (this.selected_title) {
        let selected_title_list = []

        if (this.selected_languages.length === 0) {
          selected_title_list.push(this.selected_title.name)

          return selected_title_list
        }
        else {
          for (let i = 0; i < this.selected_languages.length; i++) {
            selected_title_list.push(this.selected_title.name + ' - ' + this.selected_languages[i].name)
          }

          return selected_title_list
        }
      }
    }
  },
  watch: {
    title_type: function () {
      this.searchable_titles = []

      if (this.title_type === 'Movie') {
        for (let i = 0; i < this.titles.length; i++) {
          if (this.titles[i].type === 'movie') {
            this.searchable_titles.push(this.titles[i])
          }
        }
      } else if (this.title_type === 'Trailer') {
        for (let i = 0; i < this.titles.length; i++) {
          if (this.titles[i].type === 'trailer') {
            this.searchable_titles.push(this.titles[i])
          }
        }
      } else if (this.title_type === 'Episode') {
        for (let i = 0; i < this.titles.length; i++) {
          if (this.titles[i].type === 'episode') {
            this.searchable_titles.push(this.titles[i])
          }
        }
      }
    },
  }
}