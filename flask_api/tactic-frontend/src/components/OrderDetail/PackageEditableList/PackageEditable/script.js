/* globals localStorage */

import axios from 'axios'

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
      if (this.connectionStatus === 'disconnected') return 'Disconnected'
      else if (this.connectionStatus === 'testing') return 'Testing'
      else if (this.connectionStatus === 'connected') return 'Connected'
      else return this.connectionStatus
    },
    platformImageSource: function () {
      if (this.platformImage !== null) {
        return 'http://localhost:8081/assets/twog/platform/' + this.platformImage
      }
    }
  }
}