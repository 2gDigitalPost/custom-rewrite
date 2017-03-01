/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import DivisionEntryForm from '../DivisionEntryForm/index.vue'

import bus from '../../bus'

export default {
  name: 'ClientDetail',
  components: {
    DivisionEntryForm
  },
  data () {
    return {
      loading: true,
      clientCode: this.$route.params.code,
      clientObject: null,
      divisions: [],
      showAddDivisionForm: false
    }
  },
  methods: {
    loadClient: function () {
      var self = this

      self.loading = true
      self.clientCode = this.$route.params.code
      self.clientObject = null
      self.divisions = []
      self.showAddDivisionForm = false

      axios.get('/api/v1/client/' + self.clientCode + '/detail', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.clientObject = response.data.client
        self.divisions = self.clientObject.divisions
        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
  },
  beforeMount: function () {
    this.loadClient()
  },
  created() {
    bus.$on('reload-page', this.loadClient)
  },
  destroyed() {
    bus.$off('reload-page', this.loadClient)
  }
}