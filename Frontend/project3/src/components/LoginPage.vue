<template>
    <aside class="side_bar">
      <div class="side_bar_logo">
        <svg class="logo" viewBox="0 0 512 512" width="100%" height="100%">
          <path d="M256 403.3c-115 0-208.7-66.2-208.7-147.3S141 108.7 256 108.7 464.7 174.9 464.7 256 371 403.3 256 403.3m0-311.9C116.6 91.4 4 164.6 4 256s112.6 164.6 252 164.6 252-74 252-164.6S395.4 91.4 256 91.4" xmlns="http://www.w3.org/2000/svg"></path>
          <path d="M267 342.6h-27.6c-8.7 0-13.4-3.9-13.4-11v-63c0-3.9 1.6-5.5 5.5-5.5H267c22.3 0 40.5 17.9 40.9 40.2.3 21.5-16.9 39.1-38.4 39.4-.8 0-1.6 0-2.5-.1M226.1 182c0-7.1 4.7-11 13.4-11h18.1c18.7-.8 34.6 13.7 35.4 32.4v1.5c-.3 19.3-16.1 34.8-35.4 34.6h-26c-3.9 0-5.5-1.6-5.5-5.5v-52zm111 70.1c-5.5-2.4-5.5-3.2 0-6.3 14.1-8.7 22.5-24.3 22-40.9 0-30.7-40.9-61.4-106.3-61.4-37.8-.2-74.5 12-104.7 34.6-5.5 4.7-4.7 7.1-3.1 8.7l9.5 11c3.1 3.2 4.7 2.4 6.3.8 7.1-5.5 7.9-2.4 7.9 3.9v108.7c0 6.3-.8 9.5-7.9 3.9-1.6-1.6-3.1-2.4-6.3.8l-10.2 11.8c-1.6 2.4-3.1 4.7 3.2 8.7 31.6 21.6 68.8 33.4 107.1 33.9 73.2 0 118.9-30.7 118.9-71.7.6-27.6-22.2-41-36.4-46.5" xmlns="http://www.w3.org/2000/svg"></path>
        </svg>
      </div>

      <div class="side_bar_input">
        <Input label="Gebruikersnaam" v-model="username" text_placeholder="Celine" type="text"/>
        <Input label="Wachtwoord" v-model="password" text_placeholder="Password" type="password"/>
        <Button class="button" text="Login" @click.native="clickButton"/>
      </div>
      
      <div class="side_bar_dots">
        <div class="dots"></div>
      </div>
    </aside>
</template>
<script>
import Button from './Button.vue';
import Input from './Input.vue';

export default {
    name: 'LoginPage',
    components: {
      Button,
      Input
    },
    data: function () {
      return {
        username: '',
        password: ''
      }
    },

    methods: {
    clickButton() {
      //alert('in Button'),
      this.setLayout(this.getLoginData())
    },
    getLoginData(){
      alert('getLoginData')
      //alert(this.username + " " + this.password)
      this.$emit('login',true) // stuurd naar parent true door
    },
  },
    
}
</script>
<style scoped>
.side_bar_logo{
    width: 350px;
}
.side_bar{
  padding: 12px;
  width: 350px;
  height: 100vh;
  background-color:#006AB3;
  display: flex;
  flex-direction:column;
  justify-content: space-between;
}

.side_bar_input{
  margin: 1em;
}

.dots{
  background-image: url('data:image/svg+xml;utf8,<svg version="1.1" id="Layer_1" focusable="false" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1345.9 27" style="enable-background:new 0 0 1345.9 27;" xml:space="preserve"><circle fill="%23fff" cx="1042.9" cy="3" r="3"/><circle fill="%23fff" cx="1062.9" cy="3" r="3"/><circle fill="%23fff" cx="1082.9" cy="3" r="3"/><circle fill="%23fff" cx="1102.9" cy="3" r="3"/><circle fill="%23fff" cx="1122.9" cy="3" r="3"/><circle fill="%23fff" cx="1142.9" cy="3" r="3"/><circle fill="%23fff" cx="1162.9" cy="3" r="3"/><circle fill="%23fff" cx="1182.9" cy="3" r="3"/><circle fill="%23fff" cx="1202.9" cy="3" r="3"/><circle fill="%23fff" cx="1222.9" cy="3" r="3"/><circle fill="%23fff" cx="1242.9" cy="3" r="3"/><circle fill="%23fff" cx="1262.9" cy="3" r="3"/><circle fill="%23fff" cx="1282.9" cy="3" r="3"/><circle fill="%23fff" cx="1302.9" cy="3" r="3"/><circle fill="%23fff" cx="1322.9" cy="3" r="3"/><circle fill="%23fff" cx="1342.9" cy="3" r="3"/><circle fill="%23fff" cx="742.9" cy="3" r="3"/><circle fill="%23fff" cx="762.9" cy="3" r="3"/><circle fill="%23fff" cx="782.9" cy="3" r="3"/><circle fill="%23fff" cx="802.9" cy="3" r="3"/><circle fill="%23fff" cx="822.9" cy="3" r="3"/><circle fill="%23fff" cx="842.9" cy="3" r="3"/><circle fill="%23fff" cx="862.9" cy="3" r="3"/><circle fill="%23fff" cx="882.9" cy="3" r="3"/><circle fill="%23fff" cx="902.9" cy="3" r="3"/><circle fill="%23fff" cx="922.9" cy="3" r="3"/><circle fill="%23fff" cx="942.9" cy="3" r="3"/><circle fill="%23fff" cx="962.9" cy="3" r="3"/><circle fill="%23fff" cx="982.9" cy="3" r="3"/><circle fill="%23fff" cx="1002.9" cy="3" r="3"/><circle fill="%23fff" cx="1022.9" cy="3" r="3"/><path fill="%23fff" d="M1301.1,13.7c0,3.3-2.2,8.3-8.2,8.3c-5.3,0-8.2-5-8.2-8.6V13h-4.8v0.4c0,6.6,4.1,13.6,13,13.6c8.9,0,13-6.9,13-13.3v-0.4 h-4.8V13.7z"/><circle fill="%23fff" cx="602.9" cy="3" r="3"/><circle fill="%23fff" cx="622.9" cy="3" r="3"/><circle fill="%23fff" cx="642.9" cy="3" r="3"/><circle fill="%23fff" cx="662.9" cy="3" r="3"/><circle fill="%23fff" cx="682.9" cy="3" r="3"/><circle fill="%23fff" cx="702.9" cy="3" r="3"/><path fill="%23fff" d="M724.6,0.5c-1.4-0.9-3.2-0.6-4.2,0.8c-0.9,1.4-0.6,3.2,0.8,4.2c1,0.7,2.3,0.7,3.4,0c0.5-0.3,0.9-0.8,1.1-1.3 c0.3-0.7,0.3-1.6,0-2.3C725.5,1.3,725.1,0.8,724.6,0.5z"/><circle fill="%23fff" cx="442.9" cy="3" r="3"/><circle fill="%23fff" cx="462.9" cy="3" r="3"/><circle fill="%23fff" cx="482.9" cy="3" r="3"/><circle fill="%23fff" cx="502.9" cy="3" r="3"/><circle fill="%23fff" cx="522.9" cy="3" r="3"/><circle fill="%23fff" cx="542.9" cy="3" r="3"/><circle fill="%23fff" cx="562.9" cy="3" r="3"/><circle fill="%23fff" cx="582.9" cy="3" r="3"/><circle fill="%23fff" cx="302.9" cy="3" r="3"/><circle fill="%23fff" cx="322.9" cy="3" r="3"/><circle fill="%23fff" cx="342.9" cy="3" r="3"/><circle fill="%23fff" cx="362.9" cy="3" r="3"/><circle fill="%23fff" cx="382.9" cy="3" r="3"/><circle fill="%23fff" cx="402.9" cy="3" r="3"/><path fill="%23fff" d="M424.6,0.5c-1.4-0.9-3.2-0.6-4.2,0.8c-0.9,1.4-0.6,3.2,0.8,4.2c1,0.7,2.3,0.7,3.4,0c0.5-0.3,0.9-0.8,1.1-1.3 c0.3-0.7,0.3-1.6,0-2.3C425.5,1.3,425.1,0.8,424.6,0.5z"/><circle fill="%23fff" cx="143.1" cy="3" r="3"/><circle fill="%23fff" cx="163.1" cy="3" r="3"/><circle fill="%23fff" cx="183.1" cy="3" r="3"/><circle fill="%23fff" cx="203.1" cy="3" r="3"/><circle fill="%23fff" cx="223.1" cy="3" r="3"/><circle fill="%23fff" cx="243.1" cy="3" r="3"/><circle fill="%23fff" cx="263.1" cy="3" r="3"/><circle fill="%23fff" cx="283.1" cy="3" r="3"/><circle fill="%23fff" cx="3.1" cy="3" r="3"/><circle fill="%23fff" cx="23.1" cy="3" r="3"/><circle fill="%23fff" cx="43.1" cy="3" r="3"/><circle fill="%23fff" cx="63.1" cy="3" r="3"/><circle fill="%23fff" cx="83.1" cy="3" r="3"/><circle fill="%23fff" cx="103.1" cy="3" r="3"/><path fill="%23fff" d="M124.8,0.5c-1.4-0.9-3.2-0.6-4.2,0.8c-0.9,1.4-0.6,3.2,0.8,4.2c1,0.7,2.3,0.7,3.3,0c0.5-0.3,0.9-0.8,1.1-1.3 c0.3-0.7,0.3-1.6,0-2.3C125.7,1.3,125.3,0.8,124.8,0.5z"/></svg>');
  height: 40px;
  background-repeat: no-repeat;
  background-position: 100% 0;
  background-size: auto 27px; 
  margin-bottom:10%; 
}

.logo{
  fill: #FFFFFF;
  width: 65px;
  height: 60px;
}
.button{
  margin-top: 13%;
}
</style>
