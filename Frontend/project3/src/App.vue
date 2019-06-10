<template>
  <div id="app">
    <LoginPage v-if="!isLoggedIn" />
    <Dashboard v-else />
  </div>
</template>

<script>
import LoginPage from './components/LoginPage.vue'
import Dashboard from './components/Dashboard.vue'
const firebase = require('firebase/app')
require('firebase/auth')

export default {
  name: 'App',
  components: {
    LoginPage,
    Dashboard
  },
  data: function() {
    return {
      isLoggedIn: false
    }
  },
  created: function() {
    firebase.auth().onAuthStateChanged(user => {
      if (user) {
        console.log('Logged in')
        this.isLoggedIn = true
      } else {
        console.log('Signed out')
        this.isLoggedIn = false
      }
    })
  }
}
</script>

<style>
@font-face {
  font-family: 'CircularStd';
  src: url(assets/fonts/CircularStd-Black.woff2);
  font-weight: 900;
  font-style: normal;
}

@font-face {
  font-family: 'CircularStd';
  src: url(assets/fonts/CircularStd-BlackItalic.woff2);
  font-weight: 900;
  font-style: italic;
}

@font-face {
  font-family: 'CircularStd';
  src: url(assets/fonts/CircularStd-Bold.woff2);
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: 'CircularStd';
  src: url(assets/fonts/CircularStd-BoldItalic.woff2);
  font-weight: 700;
  font-style: italic;
}

@font-face {
  font-family: 'CircularStd';
  src: url(assets/fonts/CircularStd-Medium.woff2);
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: 'CircularStd';
  src: url(assets/fonts/CircularStd-MediumItalic.woff2);
  font-weight: 500;
  font-style: italic;
}
:root {
  --color-primary-xx-light: #f1f5f5;
  --color-primary-x-light: #ddf1fa;
  --color-primary-light: #4f95ff;
  --color-primary: #006ab3;
  --color-primary-dark: #2e77e6;
  --color-primary-x-dark: #0075c4;
  --color-primary-xx-dark: #1b3b6e;

  --color-neutral-xxxx-light: #ffffff;
  --color-neutral-xxx-light: #e2e3e7;
  --color-neutral-xx-light: #caccd4;
  --color-neutral-x-light: #b5b6c0;
  --color-neutral-light: #a0a1ad;
  --color-neutral: #8b8c9a;
  --color-neutral-dark: #757787;
  --color-neutral-x-dark: #606274;
  --color-neutral-xx-dark: #4b4c60;
  --color-neutral-xxx-dark: #35374d;
  --color-neutral-xxxx-dark: #3a3a3a;
  --color-error-message: #ea6022;

  --box-shadow: 0 2px 0 rgba(0, 0, 0, 0.2);
  --box-shadow_hover: 0 2px 0 rgba(0, 0, 0, 0.9);
}
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  height: 100%;
}
body {
  min-height: 100vh;
  background: var(--color-primary-xx-light);
  background-image: url('assets/background.png');
  background-repeat: repeat;
  overflow-x: hidden;
}
* {
  font-family: 'CircularStd', Helvetica, Arial, sans-serif;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

@media (max-width: 992px) {
  h1,
  h2 {
    font-size: 18px;
  }
  p {
    font-size: 16px;
  }
}
</style>
