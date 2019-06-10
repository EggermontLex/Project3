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
          context.commit('setLoginState', true)
          context.commit('setErrorMsg', '')
        },
        error => {
          console.log(error)
          context.commit('setLoginState', false)
          context.commit('setErrorMsg', error.message)
        }
      )
  },
  logout(context) {
    firebase
      .auth()
      .signOut()
      .then(() => {
        context.commit('setLoginState', false)
      })
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
  }
}
