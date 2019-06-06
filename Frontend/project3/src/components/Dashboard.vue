<template>
  <div class="page">
    <div class="logo">
      <img src="../assets/logo_nmbs.png" alt="logo nmbs" class="logo_img"/>
    </div>
    <Button class="button" text="Logout" @click.native="Logout"/>
    <div class="container">
      <div class="cards">
        <Card v-for="trainid in trainIds" v-bind:key="trainid" :trainId="trainid"/>
      </div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue';
import Button from './Button.vue';
import {myFunctions} from '../main.js';
const firebase = require("firebase/app");
require("firebase/auth");

export default {
  name: 'Dashboard',
  components: {
    Card,
    Button
  },
  created: async function(){
     let data = await myFunctions.getCollectionDocs('realtime')
     for (let i = 0; i < data.docs.length; i++){
      //console.log('Data',)
      this.trainIds.push( data.docs[i].id)
     }
     //console.log(this.trainIds)
        
  },
  data:function(){
    return{
      trainIds: []
    }
  },
  methods:{
    Logout(){
      firebase.auth().signOut().then(() => {
        this.$emit('login',false) 
      }).catch(function(error) {
        console.log(error)
      });
    }
  }
}
</script>

<style scoped>
.page{
  display: flex;
  justify-content:space-between;
  flex-direction:column;
}
.top-bar{
  padding: 12px;
}
.logo{
  margin:12px; 
  position: absolute;
  width: 65px;
}
.logo_img{
  width: 65px;
}
.button{
  margin:12px; 
  background-color: var(--color-primary);
  color: var(--color-neutral-xxxx-light);
  width: 150px;
  position: absolute;
  right: 0;
}
.button:hover, .button:active{
  box-shadow: 0 2px 0 rgba(0,0,0,.2);
  color: var(--color-neutral-xxxx-light);
  background-color: var(--color-primary-x-dark);
}
.container{
  height: 100vh;
  width: 100vw;
  padding-top: 60px;
  display: flex;
  justify-content:space-between;
  flex-direction:column;
}
.cards{
  display: flex;
  flex-direction: column;
  align-items: center
}
.card{
  max-width: 950px;
}
.update{
  display: flex;
  justify-content:flex-end;
  padding: 12px;
}
@media (max-width: 768px) {
  .card {
    padding: 0;
    width: 100%;
  }
}

</style>
