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
    updateSelectedTitle: function (newSelectedTitle) {
      this.selected_title = newSelectedTitle
    },
    updateSelectedLanguages: function (newSelectedLanguage) {
      this.selected_language = newSelectedLanguage
    },
    addComponentsToTactic: function() {
      var self = this
      let components_to_send = []
      let order_code = self.$route.params.code

      if (this.selected_languages.length === 0) {
        let component = {
          'name': this.selected_title.name,
          'title_code': this.selected_title.code,
          'pipeline_code': this.selected_pipeline.code
        }

        components_to_send.push(component)
      }
      else {
        for (let i = 0; i < this.selected_languages.length; i++) {
          let component = {
            'name': this.selected_title.name + ' - ' + this.selected_languages[i].name,
            'title_code': this.selected_title.code,
            'language_code': this.selected_languages[i].code,
            'pipeline_code': this.selected_pipeline.code
          }

          components_to_send.push(component)
        }
      }

      console.log(components_to_send)

      let apiURL = '/api/v1/orders/' + order_code + '/components'
      let json_to_send = {
        'token': localStorage.tactic_token,
        'components': components_to_send
      }

      axios.post(apiURL, JSON.stringify(json_to_send), {
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
      if (this.selected_title) {
        let created_components_list = []

        if (this.selected_languages.length === 0) {
          created_components_list.push(this.selected_title.name)

          return created_components_list
        }
        else {
          for (let i = 0; i < this.selected_languages.length; i++) {
            created_components_list.push(this.selected_title.name + ' - ' + this.selected_languages[i].name)
          }

          return created_components_list
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