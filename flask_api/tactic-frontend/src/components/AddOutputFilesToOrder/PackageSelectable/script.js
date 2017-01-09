/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

import bus from '../../../bus'

export default {
  name: 'PackageSelectable',
  props: ['package', 'selected', 'externallySelected'],
  methods: {
    packageSelected: function () {
      bus.$emit('package-selected', this.package.code)
    }
  },
  created() {
    bus.$on('highlight-packages', this.fileFlowSelected)
  },
  destroyed() {
    bus.$off('highlight-packages', this.fileFlowSelected)
  }
}