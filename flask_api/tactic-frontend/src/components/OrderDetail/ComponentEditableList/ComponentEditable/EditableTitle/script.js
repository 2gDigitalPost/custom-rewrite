/* globals localStorage */

import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../../../bus'

export default {
  name: 'EditableTitle',
  props: ['title', 'componentCode'],
  components: {
    Multiselect
  },
  data () {
    return {
      editing: false,
      loading: false,
      selectableTitles: [],
      selectedTitle: null
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
          self.selectableTitles.push({name: titleData[i].name, code: titleData[i].code})
        }

        for (let i = 0; i < self.selectableTitles.length; i++) {
          if (self.selectableTitles[i].code === self.title.code) {
            self.selectedTitle = self.title
          }
        }

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function () {
      let self = this

      let apiURL = '/api/v1/components/' + self.componentCode
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'component': {
          'title_code': self.selectedTitle.code
        }
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

            bus.$emit('component-title-updated')
          }
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  watch: {
    editing: function () {
      let self = this

      if (self.editing && self.selectableTitles.length === 0) {
        self.loadTitles()
      }
    }
  }
}