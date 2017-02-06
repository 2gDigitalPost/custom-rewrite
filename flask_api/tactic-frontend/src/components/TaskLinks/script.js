/* globals localStorage */

import axios from 'axios'

export default {
  name: 'TaskLinks',
    data () {
    return {
      edel: '/tasks/edel',
      compression: '/tasks/compression',
      qc: '/tasks/qc',
      onboarding: '/tasks/onboarding',
      all: '/tasks',
      my: '/tasks/user'
    }
  }
}