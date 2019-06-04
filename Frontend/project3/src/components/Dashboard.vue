<template>
  <div class="page">
    <div class="logo">
      <img src="../assets/logo_nmbs.png" alt="logo nmbs" class="logo_img"/>
    </div>
    <Button class="button" text="Logout" @click.native="clickButton"/>
    <div class="container">
      <div class="cards">
        <Card/>
      </div>
      <div class="update">
        <p>Laatst upgedate op: <b class="update_text">10:00:00 03/06/2019</b></p>
      </div>
      
    </div>
  </div>
</template>

<script>
import Card from './Card.vue';
import Button from './Button.vue';

export default {
  name: 'Dashboard',
  components: {
    Card,
    Button
  },
  methods:{
    clickButton() {
      //alert('in Button'),
      this.Logout()
    },
    Logout(){
      this.$emit('login',false) 
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

</style>
