/* globals localStorage */

import axios from 'axios'

export default {
  name: 'DepartmentRequestLinks',
    data () {
    return {
      edel_link: '/department-requests/edel',
      compression_link: '/department-requests/compression',
      qc_link: '/department-requests/qc',
      onboarding_link: '/department-requests/onboarding'
    }
  }
}