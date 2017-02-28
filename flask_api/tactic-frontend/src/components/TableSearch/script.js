/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'
import moment from 'moment'
import Multiselect from 'vue-multiselect'

import bus from '../../bus'

export default {
  name: 'TableSearch',
  props: ['options'],
  components: {
    Multiselect
  },
  data () {
    return {
      selectedSearchOption: null,
      searchQueryText: null,
      selectedMultiselectOptions: null
    }
  },
  methods: {
    setDefaultSearchOption: function () {
      if (this.options.length > 0) {
        this.selectedSearchOption = this.options[0]
      }
    },
    getOptionLabel: function (option) {
      if (option.hasOwnProperty('label')) {
        return option['label']
      }
      else {
        return _.startCase(_.toLower(option['name']))
      }
    }
  },
  computed: {
    selectedSearchName: function () {
      if (this.selectedSearchOption) {
        return this.selectedSearchOption['name']
      }
    },
    selectedSearchType: function () {
      if (this.selectedSearchOption) {
        return this.selectedSearchOption['type']
      }
    },
    searchMultiselectOptions: function () {
      if (this.selectedSearchOption && this.selectedSearchOption['type'] === 'select') {
        return this.selectedSearchOption['options']
      }
    }
  },
  watch: {
    searchQueryText: function () {
      if (this.selectedSearchType === 'text') {
        bus.$emit('search-query', this.selectedSearchName, this.searchQueryText)
      }
    },
    selectedMultiselectOptions: function () {
      if (this.selectedSearchType === 'select') {
        bus.$emit('search-query', this.selectedSearchName, _.map(this.selectedMultiselectOptions, 'value'))
      }
    }
  },
  beforeMount: function () {
    this.setDefaultSearchOption()
  }
}