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

        axios.post('/api/v1/login', {
          username: this.username,
          password: this.password
        })
        .then(function (response) {
          localStorage.setItem('tactic_token', response.data.ticket)
          localStorage.setItem('login', self.username)

          self.$router.replace(self.$route.query.redirect || '/')
        })
        .catch(function (error) {
          console.log(error)
        })
      }
    }
  }
</script>
