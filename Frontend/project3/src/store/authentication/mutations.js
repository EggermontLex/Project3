import Vue from 'vue'

export const mutations = {
  setLoginState(state, isLoggedIn) {
    Vue.set(state, 'authentication', isLoggedIn)
  }
}
