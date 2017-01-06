/* globals localStorage */

import axios from 'axios'

export default {
  name: 'PackageSelectable',
  props: ['package'],
  data () {
    return {
      selected: false
    }
  }
}