/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../bus'

export default {
  name: 'FileFlowEntryForm',
  props: ['componentCode', 'orderCode'],
  data () {
    return {
      loading: true,
      name: null,
      packageOptions: [],
      selectedPackages: [],
    }
  },
  methods: {
    loadPackageOptions: function () {
      let self = this

      self.loading = true

      axios.get('/api/v1/order/' + self.orderCode + '/packages', {
        params: {
          token: localStorage.tactic_token,
        }
      })
      .then(function (response) {
        self.packageOptions = response.data.packages

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submit: function () {
      let self = this

      let jsonToSubmit = {
        'token': localStorage.tactic_token,
        'file_flow': {
          'name': self.name,
          'component_code': self.componentCode,
        },
        'package_codes': self.selectedPackages
      }

      axios.post('/api/v1/file-flows', jsonToSubmit, {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          bus.$emit('reload-page')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancel: function () {
      bus.$emit('file-flow-entry-cancel')
    }
  },
  beforeMount: function () {
    this.loadPackageOptions()
  }
}