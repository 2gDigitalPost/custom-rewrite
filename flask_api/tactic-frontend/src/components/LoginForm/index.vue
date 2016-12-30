<template src="./template.html"></template>
<style></style>
<script>
  /* globals localStorage */

  import axios from 'axios'

  export default {
    name: 'LoginForm',
    data () {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      getToken: function () {
        let self = this

        axios.post('http://0.0.0.0:5000/api/v1/login', {
          username: this.username,
          password: this.password
        })
        .then(function (response) {
          localStorage.setItem('tactic_token', response.data.ticket)

          self.$router.replace(self.$route.query.redirect || '/')
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    }
  }
</script>
