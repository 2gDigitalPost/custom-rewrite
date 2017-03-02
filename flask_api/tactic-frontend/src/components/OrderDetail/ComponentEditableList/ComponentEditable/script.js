/* globals localStorage */

import axios from 'axios'

import EditableTitle from './EditableTitle/index.vue'
import TaskEditableList from './TaskEditableList/index.vue'
import FileFlowEditableList from '../../../FileFlowEditableList/index.vue'
import FileFlowEntryForm from '../../../FileFlowEntryForm/index.vue'

import bus from '../../../../bus'

export default {
  name: 'ComponentEditable',
  props: ['component'],
  components: {
    EditableTitle,
    TaskEditableList,
    FileFlowEditableList,
    FileFlowEntryForm
  },
  data () {
    return {
      componentObject: this.component.component,
      fileFlows: this.component.file_flows,
      tasks: this.component.tasks,
      title: this.component.title,
      instructionsDocument: this.component,
      addingFileFlow: false
    }
  },
  methods: {
    loadInstructionsPage: function () {
      let instructionsPageURL = '/instructions/' + this.component.component.instructions_code

      this.$router.push(instructionsPageURL)
    },
    removeComponent: function () {
      let self = this

      let confirmation = window.confirm('Are you sure you want to remove the component "' + self.componentObject.name + '"?')

      let apiURL = '/api/v1/remove/twog/component'
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'code': self.component.code
      }

      if (confirmation) {
        axios.post(apiURL, JSON.stringify(jsonToSend), {
          headers: {
            'Content-Type': 'application/json;charset=UTF-8'
          }
        })
        .then(function (response) {
          if (response.data) {
            if (response.data.status === 200) {
              bus.$emit('component-removed')
            }
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    },
    cancelFileFlowEntry: function () {
      this.addingFileFlow = false
    }
  },
  created() {
    bus.$on('file-flow-entry-cancel', this.cancelFileFlowEntry)
  },
  destroyed() {
    bus.$off('file-flow-entry-cancel', this.cancelFileFlowEntry)
  }
}