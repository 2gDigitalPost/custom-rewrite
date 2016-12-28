<template>
    <div>
        <select v-model="selected_client">
            <option v-for="option in client_options" v-bind:value="option.value">
                {{ option.text }}
            </option>
        </select>
        <span>Selected: {{ selected_client }}</span>
    </div>
</template>
<style>
</style>
<script>
  /* globals localStorage */

  import axios from 'axios'

  export default {
    name: 'ClientSelect',
    data () {
      return {
        selected_client: '',
        client_options: []
      }
    },
    methods: {
      loadClients: function () {
        var self = this

        axios.get('http://localhost:5000/api/v1/clients', {
          params: {
            token: localStorage.tactic_token
          }
        })
        .then(function (response) {
          console.log(response)

          let clientData = response.data.clients

          for (let i = 0; i < clientData.length; i++) {
            self.client_options.push({text: clientData[i].name, value: clientData[i].code})
          }
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    },
    beforeMount: function () {
      this.loadClients()
    }
  }
</script>
