const firebase = require('firebase/app')
require('firebase/auth')

export const actions = {
  login(context, email, password) {
    console.log(email)
    firebase
      .auth()
      .signInWithEmailAndPassword(email, password)
      .then(
        user => {
          console.log(user)
          context.commit('setLoginState', true)
        },
        error => {
          console.log(error)
          context.commit('setLoginState', false)
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
  }
}
