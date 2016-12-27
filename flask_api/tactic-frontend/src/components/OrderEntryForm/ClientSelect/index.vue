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
        /* $.get('/api/v1/clients', function (response) {
          for (var i = 0; i < response.clients.length; i++) {
            this.client_options.push({text: response.clients[i].name, value: response.clients[i].code})
          }
        }.bind(this)) */
        /* axios.get('http://localhost:5000/api/v1/clients', function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        }) */
      }
    },
    beforeMount: function () {
      this.loadClients()
    }
  }
</script>
