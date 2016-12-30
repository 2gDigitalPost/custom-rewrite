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
      selected_title: '',
      titles: [],
      searchable_titles: ['asdf'],
      search_options: []
    }
  },
  methods: {
    loadTitles: function () {
      var self = this

      axios.get('http://0.0.0.0:5000/api/v1/titles', {
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
    }
  },
  beforeMount: function () {
    this.loadTitles()
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
    }
  }
}