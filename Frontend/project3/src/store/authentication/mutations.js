import Vue from 'vue'

export const mutations = {
  setLoginState(state, isLoggedIn) {
    Vue.set(state, 'isLoggedIn', isLoggedIn)
  },
  setErrorMsg(state, msg) {
    Vue.set(state, 'errorMsg', msg)
  }
}
