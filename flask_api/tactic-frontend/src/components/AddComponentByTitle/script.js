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
      title_type: null,
      selectedTitles: [],
      selectedLanguages: [],
      titles: [],
      searchable_titles: [],
      languages: [],
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
    addComponentsToTactic: function() {
      var self = this
      let componentsToSend = []
      let orderCode = self.$route.params.code

      _.forEach(self.selectedTitles, function(selectedTitle) {
        let component = {
          'name': selectedTitle.name,
          'title_code': selectedTitle.code
        }
        
        if (self.selected_pipeline) {
          component['pipeline_code'] = self.selected_pipeline.code
        }

        if (self.selectedLanguages.length > 0) {
          _.forEach(self.selectedLanguages, function(selectedLanguage) {
            component['name'] = component['name'] + ' - ' + selectedLanguage.name
            component['language_code'] = selectedLanguage.code

            componentsToSend.push(component)
          })
        }
        else {
          componentsToSend.push(component)
        }
      })

      let apiURL = '/api/v1/orders/' + orderCode + '/components'
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'components': componentsToSend
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
    this.loadPipelines()
  },
  computed: {
    created_components: function() {
      let self = this
      let createdComponentsList = []

      _.forEach(self.selectedTitles, function(selectedTitle) {
        if (self.selectedLanguages.length > 0) {
          _.forEach(self.selectedLanguages, function(selectedLanguage) {
            createdComponentsList.push(selectedTitle.name + ' - ' + selectedLanguage.name)
          })
        }
        else {
          createdComponentsList.push(selectedTitle.name)
        }
      })

      return createdComponentsList
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