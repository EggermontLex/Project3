<template>
  <div id="app">
    
    <Button text="dit is tekst!!!!"/>

  </div>
</template>

<script>
import Button from './components/Button.vue';

export default {
  name: 'app',
  components: {
    Button
  }
}

</script>

<style>
#app {
  font-family: 'CircularStd', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
* {
  padding: 0;
  margin: 0;
}

@font-face {
  font-family: CircularStd;
  src: url(assets/fonts/CircularStd-Black.ttf);
  font-weight: 900;
  font-style: normal;
}

@font-face {
  font-family: CircularStd;
  src: url(assets/fonts/CircularStd-BlackItalic.ttf);
  font-weight: 900;
  font-style: italic;
}

@font-face {
  font-family: CircularStd;
  src: url(assets/fonts/CircularStd-Bold.ttf);
  font-weight: 700;
  font-style: normal;
}

@font-face {
  font-family: CircularStd;
  src: url(assets/fonts/CircularStd-BoldItalic.ttf);
  font-weight: 700;
  font-style: italic;
}

@font-face {
  font-family: CircularStd;
  src: url(assets/fonts/CircularStd-Medium.ttf);
  font-weight: 500;
  font-style: normal;
}

@font-face {
  font-family: CircularStd;
  src: url(assets/fonts/CircularStd-MediumItalic.ttf);
  font-weight: 500;
  font-style: italic;
}
</style>
