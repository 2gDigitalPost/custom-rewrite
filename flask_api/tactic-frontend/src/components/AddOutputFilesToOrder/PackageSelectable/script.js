/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../../bus'

export default {
  name: 'PackageSelectable',
  props: ['package'],
  data () {
    return {
      selected: false,
      externallySelected: false
    }
  },
  methods: {
    fileFlowSelected: function (packageCodes, selected) {
      if (_.includes(packageCodes, this.package.code)) {
        this.externallySelected = selected
      }
    }
  },
  created() {
    bus.$on('highlight-packages', this.fileFlowSelected)
  },
  destroyed() {
    bus.$off('highlight-packages', this.fileFlowSelected)
  }
}