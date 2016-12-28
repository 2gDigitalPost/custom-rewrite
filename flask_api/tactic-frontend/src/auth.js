/* globals localStorage */

export default {
  getToken () {
    return localStorage.getItem('tactic_token')
  },
  loggedIn () {
    return !!localStorage.tactic_token
  },
  logout () {
    delete localStorage.tactic_token
  }
}
