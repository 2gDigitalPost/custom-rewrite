/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import marked from 'marked'

import bus from '../../bus'

export default {
  name: 'EditableEstimatedHours',
  props: ['currentEstimatedHours', 'taskDataCode'],
  data () {
    return {
      editing: false,
      newEstimatedHours: this.currentEstimatedHours
    }
  },
  methods: {
    submitToTactic: function () {
      let self = this

      axios.post('/api/v1/estimated-hours', 
        JSON.stringify({
          'task_data_code': self.taskDataCode,
          'estimated_hours': self.newEstimatedHours,
          'token': localStorage.tactic_token
        }), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      })
      .then(function (response) {
        if (response.status === 200) {
          // Reload the page
          bus.$emit('estimated-hours-updated')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    }
  }
}