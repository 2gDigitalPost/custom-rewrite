/* globals localStorage */

import bus from '../../../bus'

import axios from 'axios'
import _ from 'lodash'
import Multiselect from 'vue-multiselect'

export default {
  name: 'EquipmentInTask',
  props: ['task', 'currentEquipment'],
  components: {
    Multiselect,
  },
  data () {
    return {
      selectedEquipment: [],
      equipmentOptions: [],
      loading: true,
      submitting: false
    }
  },
  methods: {
    loadEquipment: function () {
      let self = this

      self.loading = true

      self.selectedEquipment = self.currentEquipment
      self.equipmentOptions = []

      axios.get('/api/v1/equipment', {
        params: {
          token: localStorage.tactic_token,
        }
      })
      .then(function (response) {
        console.log(response)
        let equipmentData = response.data.equipment

        for (let i = 0; i < equipmentData.length; i++) {
          self.equipmentOptions.push({name: equipmentData[i].name, code: equipmentData[i].code})
        }

        self.equipmentOptions = _.sortBy(self.equipmentOptions, 'name')

        self.loading = false
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    submitToTactic: function () {
      let self = this

      let apiURL = '/api/v1/task/' + self.task.code + '/equipment'
      let equipmentCodes = _.map(self.selectedEquipment, 'code')
      let jsonToSend = {
        'token': localStorage.tactic_token,
        'equipment_codes': equipmentCodes
      }

      self.submitting = true

      axios.post(apiURL, JSON.stringify(jsonToSend), {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        },
      })
      .then(function (response) {
        if (response.status === 200) {
          self.submitting = false

          bus.$emit('equipment-changed')
        }
      })
      .catch(function (error) {
        console.log(error)
      })
    },
    cancelEdit: function () {
      bus.$emit('equipment-edit-cancel')
    }
  },
  beforeMount: function () {
    this.loadEquipment()
  }
}