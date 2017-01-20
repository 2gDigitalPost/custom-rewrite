/* globals localStorage */

import axios from 'axios'

import bus from '../../../bus'

export default {
  name: 'EditableFileFlowTemplate',
  props: ['fileFlowTemplate'],
  data () {
    return {
      editing: false,
      code: this.fileFlowTemplate.code,
      name: this.fileFlowTemplate.name,
    }
  },
  methods: {
    deleteFileFlowTemplate: function () {
      let self = this

      let confirmation = window.confirm('Are you sure you want to delete the file flow "' + self.name + '"?')

      if (confirmation) {
        axios.delete('/api/v1/file-flow-templates/' + self.code,
        {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8'
          },
          params: {
            token: localStorage.tactic_token,
          }
        })
        .then(function (response) {
          if (response.data) {
            if (response.data.status === 200) {
              bus.$emit('file-flow-template-updated')
            }
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    }
  }
}
