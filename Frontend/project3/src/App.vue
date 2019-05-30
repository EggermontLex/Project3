<template>
  <div id="app">
    <aside class="side_bar">
      <Input label="Gebruikersnaam" text_placeholder="Celine" type="text"/>
      <Input label="Wachtwoord" text_placeholder="Password" type="password"/>
      <Button text="dit is tekst!!!!"/>
    </aside>
    <main>
      <Card/>
    </main>
  </div>
</template>

<script>
import Button from './components/Button.vue';
import Input from './components/Input.vue';
import Card from './components/Card.vue';

export default {
  name: 'app',
  components: {
    Button,
    Input,
    Card
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
}
* {
  font-family: 'CircularStd', Helvetica, Arial, sans-serif;
  padding: 0;
  margin: 0;
}

.side_bar{
  width: 500px;
  padding: 12px;
}

.side_bar{
  background-color:#006AB3;
}
</style>
