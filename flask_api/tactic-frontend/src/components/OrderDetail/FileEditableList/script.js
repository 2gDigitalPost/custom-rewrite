/* globals localStorage */

import NewFileForm from '../../NewFileForm/index.vue'
import ImportFileToOrder from '../../ImportFileToOrder/index.vue'
import FileEditable from './FileEditable/index.vue'

import _ from 'lodash'
import axios from 'axios'
import Multiselect from 'vue-multiselect'

import bus from '../../../bus'

export default {
  name: 'FileEditableList',
  props: ['files', 'orderCode', 'divisionCode'],
  components: {
    NewFileForm,
    ImportFileToOrder,
    FileEditable,
    Multiselect
  },
  data () {
    return {
      creatingNewFile: false,
      importingFiles: false
    }
  },
  methods: {
    filterFilesByClassification: function (classification) {
      return _.filter(this.files, function(file) { return _.lowerCase(file['classification']) === classification })
    },
    cancelEdit: function () {
      this.creatingNewFile = false
    },
    cancelImport: function () {
      this.importingFiles = false
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
  },
  created() {
    bus.$on('new-file-entry-cancel', this.cancelEdit)
    bus.$on('file-import-cancel', this.cancelImport)
  },
  destroyed() {
    bus.$off('new-file-entry-cancel', this.cancelEdit)
    bus.$off('file-import-cancel', this.cancelImport)
  }
}