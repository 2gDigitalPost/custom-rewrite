/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

import bus from '../../../../bus'

export default {
  name: 'PackageEntryForm',
  props: ['orderCode'],
  components: {
    'multiselect': Multiselect,
  },
  data () {
    return {
      loading: false,
      name: null,
      selectedPlatform: null,
      selectedPipeline: null,
      platformOptions: [],
      pipelineOptions: [],
      errors: []
    }
  },
  methods: {
    loadPlatformOptions: function () {
      let self = this

      axios.get('/api/v1/platforms', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.platformOptions = response.data.platforms
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    loadPipelineOptions: function () {
      var self = this

      axios.get('/api/v1/pipelines/package', {
        params: {
          token: localStorage.tactic_token
        }
      })
      .then(function (response) {
        self.pipelineOptions = response.data.pipelines
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submit: function () {
      let self = this
      self.errors = []

      if (!self.name) {
        self.errors.push('name')
      }
      if (!self.selectedPlatform) {
        self.errors.push('platform')
      }
      if (!self.selectedPipeline) {
        self.errors.push('pipeline')
      }

      if (self.errors.length > 0) {
        return
      }

      let jsonToSend = {
        'token': localStorage.tactic_token,
        'package': {
          'name': self.name,
          'order_code': self.orderCode,
          'platform_code': self.selectedPlatform.code,
          'pipeline_code': self.selectedPipeline.code,
        }
      }

      axios.post('/api/v1/packages',
        JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.status === 200) {
          // Reload the page
          bus.$emit('reload-page')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  },
  beforeMount: function () {
    this.loading = true
    
    this.loadPlatformOptions()
    this.loadPipelineOptions()

    this.loading = false
  },
  computed: {
    nameError: function () {
      if (_.includes(this.errors, 'name')) return true
      else return false
    },
    platformError: function () {
      if (_.includes(this.errors, 'platform')) return true
      else return false
    },
    pipelineError: function () {
      if (_.includes(this.errors, 'pipeline')) return true
      else return false
    }
  }
}