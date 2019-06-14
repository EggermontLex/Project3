const firebase = require('firebase/app')
require('firebase/auth')

export const actions = {
  login(context, credentials) {
    firebase
      .auth()
      .signInWithEmailAndPassword(credentials.email, credentials.password)
      .then(
        user => {
          console.log(user)
          context.commit('setErrorMsg', '')
        },
        error => {
          console.log(error)
          context.commit('setErrorMsg', error.message)
        }
      )
  },
  logout() {
    firebase
      .auth()
      .signOut()
      .catch(error => {
        console.log(error)
      })
  },
  fetchCreds(context) {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        console.log('Logged in')
        context.commit('setLoginState', true)
      } else {
        console.log('Signed out')
        context.commit('setLoginState', false)
      }
    })
  },
  setAdminState(context, isAdmin) {
    context.commit('setAdminState', isAdmin)
  }
}
