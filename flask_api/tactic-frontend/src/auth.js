/* globals localStorage */

export default {
  getToken () {
    return localStorage.getItem('tactic_token')
  },
  getLogin () {
    return localStorage.getItem('login')
  },
  loggedIn () {
    return !!localStorage.tactic_token
  },
  logout () {
    delete localStorage.tactic_token
    delete localStorage.login
  }
}
