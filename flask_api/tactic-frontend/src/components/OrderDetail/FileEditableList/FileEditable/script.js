/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'FileEditable',
  props: ['file', 'orderCode'],
  data () {
    return {
      editing: false,
      editName: null,
      editPath: null
    }
  },
  methods: {
    submitChanges: function () {

    },
    removeFileFromOrder: function () {
      let self = this
    }
  }
}