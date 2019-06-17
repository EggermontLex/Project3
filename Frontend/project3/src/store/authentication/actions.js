const firebase = require('firebase/app')
require('firebase/auth')

export const actions = {
  login(context, credentials) {
    firebase
      .auth()
      .signInWithEmailAndPassword(credentials.email, credentials.password)
      .then(
        user => {
          context.commit('setErrorMsg', '')
        },
        error => {
          context.commit('setErrorMsg', error.message)
        }
      )
  },
  logout() {
    firebase.auth().signOut()
  },
  fetchCreds(context) {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        context.commit('setLoginState', true)
      } else {
        context.commit('setLoginState', false)
      }
    })
  },
  setAdminState(context, isAdmin) {
    context.commit('setAdminState', isAdmin)
  }
}
