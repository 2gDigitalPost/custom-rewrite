/* globals localStorage */

import axios from 'axios'
import _ from 'lodash'

export default {
  name: 'PackageEditable',
  props: ['package'],
  data () {
    return {
      connectionStatus: this.package.platform_connection.connection_status,
      platformImage: this.package.platform_image
    }
  },
  methods: {

  },
  computed: {
    connectionStatusText: function () {
      return _.startCase(this.connectionStatus)
    },
    platformImageSource: function () {
      if (this.platformImage !== null) {
        return 'http://localhost:8081/assets/twog/platform/' + this.platformImage
      }
    }
  }
}