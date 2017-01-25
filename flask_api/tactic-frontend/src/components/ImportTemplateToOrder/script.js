/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'ImportTemplateToOrder',
  components: {
    Multiselect
  },
  data () {
    return {
      title_type: null,
      selectedTitles: [],
      selectedLanguages: [],
      titles: [],
      searchable_titles: [],
      languages: [],
      selectedProjectTemplate: null,
      projectTemplates: []
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
    submitToTactic: function () {
      var self = this

      let orderCode = self.$route.params.code

      let apiURL = '/api/v1/orders/' + orderCode + '/create-from-template'
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'titles': self.selectedTitles,
        'languages': self.selectedLanguages,
        'project_template_code': self.selectedProjectTemplate.code
      }

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.data) {
          if (response.data.status === 200) {
            console.log(response.data)
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loadTitles()
    this.loadLanguages()
    this.loadProjectTemplates()
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