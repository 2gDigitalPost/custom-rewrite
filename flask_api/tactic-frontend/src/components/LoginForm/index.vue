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
        axios.post('http://localhost:5000/api/v1/login', {
          username: this.username,
          password: this.password
        })
        .then(function (response) {
          console.log(response.data.ticket)

          localStorage.setItem('tactic_token', response.data.ticket)

          console.log(localStorage.getItem('tactic_token'))

          this.$route.router.replace(this.$route.query.redirect || '/')
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    }
  }
</script>
