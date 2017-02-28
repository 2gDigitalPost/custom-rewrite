/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../bus'

export default {
  name: 'PlatformEntryForm',
  data () {
    return {
      loading: false,
      searching: false,
      name: '',
      errors: [],
      nameExists: false
    }
  },
  methods: {
    getExistingPlatform: _.debounce(
      function () {
        let self = this

        if (self.name === '') {
          self.searching = false
          return
        }

        axios.get('/api/v1/platform/name/' + self.name + '/exists', {
          params: {
            token: localStorage.tactic_token
          }
        })
        .then(function (response) {
          console.log(response)
          if (response.data.exists) {
            self.nameExists = true
          }
          else {
            self.nameExists = false
          }

          self.searching = false
        })
        .catch(function (error) {
          console.log(error)
        })
      }, 500
    ),
    submit: function () {
      let self = this

      let jsonData = {
        'token': localStorage.tactic_token,
        'platform': {
          'name': self.name,
        }
      }

      axios.post('/api/v1/platforms', JSON.stringify(jsonData), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.data.status === 200) {
          bus.$emit('reload-page')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  watch: {
    name: function () {
      this.searching = true
      this.getExistingPlatform()
    }
  }
}