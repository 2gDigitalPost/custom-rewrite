/* globals localStorage */

import axios from 'axios'

export default {
  name: 'PackageEditable',
  props: ['package'],
  data () {
    return {
      connectionStatus: this.package.platform_connection.connection_status
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
    }
  }
}