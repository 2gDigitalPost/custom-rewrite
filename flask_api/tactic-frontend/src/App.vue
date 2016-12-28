<template>
  <div id="app">
    <img src="./assets/logo.png">

    <ul>
      <li>
        <router-link v-if="loggedIn" to="/logout">Log Out</router-link>
        <router-link v-if="!loggedIn" to="/login">Log In</router-link>
      </li>
      <li>
        <router-link to="/order_entry">Enter a new Order</router-link>
      </li>
      <li>
        <router-link to="/about">About</router-link>
      </li>
    </ul>
    <router-view class="view"></router-view>
  </div>
</template>

<script>
import auth from './auth'

export default {
  name: 'app',
  data () {
    return {
      loggedIn: auth.loggedIn()
    }
  },
  created () {
    auth.onChange = loggedIn => {
      this.loggedIn = loggedIn
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
