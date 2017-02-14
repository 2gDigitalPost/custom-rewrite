/* globals localStorage */

import FileEditable from './FileEditable/index.vue'

import _ from 'lodash'

export default {
  name: 'FileEditableList',
  props: ['files'],
  components: {
    FileEditable
  },
  methods: {
    filterFilesByClassification: function (classification) {
      return _.filter(this.files, function(file) { return _.lowerCase(file['classification']) === classification })
    }
  },
  computed: {
    sourceFiles: function () {
      return this.filterFilesByClassification('source')
    },
    intermediateFiles: function () {
      return this.filterFilesByClassification('intermediate')
    },
    deliverableFiles: function () {
      return this.filterFilesByClassification('deliverable')
    }
  }
}