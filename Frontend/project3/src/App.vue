<template>
  <div id="app">
    <LoginPage v-on:login="setLayout" v-if="!isLoggedIn"/>
    <Dashboard v-on:login="setLayout" v-if="isLoggedIn"/>
  </div>
</template>

<script>
import LoginPage from './components/LoginPage.vue';
import Dashboard from './components/Dashboard.vue';

export default {
  name: 'app',
  components: {
    LoginPage,
    Dashboard
  },
  data:function(){
    return{
      isLoggedIn: false
    }
  },

  methods:{
    setLayout(isLoggedIn){
      //alert('in setLayout')
      //alert(isLoggedIn)
      this.isLoggedIn = isLoggedIn
    }
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

#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  display: flex;
  height: 100%;
}
body{
  min-height: 100vh;
  background: #F1F5F5;
  background-image: url("assets/background.png");
  background-repeat: repeat;
  overflow-x: hidden;

}
* {
  font-family: 'CircularStd', Helvetica, Arial, sans-serif;
  padding: 0;
  margin: 0;
  box-sizing: border-box;
}

</style>
