<template>
  <div id="app">
    <nav class="navbar navbar-default">
      <div class="container-fluid">
        <!-- Brand and toggle get grouped for better mobile display -->
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1" aria-expanded="false">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <router-link to="/" class="navbar-brand">Tactic</router-link>
        </div>

        <!-- Collect the nav links, forms, and other content for toggling -->
        <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
          <ul class="nav navbar-nav">
            <li>
              <router-link v-if="loggedIn" to="/logout">Log Out</router-link>
              <router-link v-if="!loggedIn" to="/login">Log In</router-link>
            </li>
            <li>
              <router-link to="/orders">Orders</router-link>
            </li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Tasks <span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><router-link to="/tasks">All</router-link></li>
                <li role="separator" class="divider"/>
                <li class="dropdown-header">By Department</li>
                <li><router-link to="/tasks/edel">Edel</router-link></li>
                <li><router-link to="/tasks/compression">Compression</router-link></li>
                <li><router-link to="/tasks/qc">QC</router-link></li>
                <li><router-link to="/tasks/onboarding">Onboarding</router-link></li>
              </ul>
            </li>
            <li>
              <router-link to="/department-requests/links">Department Requests</router-link>
            </li>
            <li>
              <router-link to="/project-templates">Project Templates</router-link>
            </li>
            <li>
              <router-link to="/instructions-templates">Instructions Templates</router-link>
            </li>
          </ul>
        </div><!-- /.navbar-collapse -->
      </div><!-- /.container-fluid -->
    </nav>
    <router-view class="container"></router-view>
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

<script src="../node_modules/bootstrap/dist/js/bootstrap.min.js"></script>

<style src='../node_modules/bootstrap/dist/css/bootstrap.css'></style>
<style src='../node_modules/font-awesome/css/font-awesome.min.css'></style>
