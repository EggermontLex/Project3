<template>

      <div class="card">
          <div class="topbar">
            <h1>Huidige waarden</h1>
            <p class="update">Laatst geüpdate: <b class="update_text">{{ time }}</b></p>
          </div>
          <p>Aantal mensen:</p>
          <h2>{{value}}</h2>
          
          <div class="grafiek">
            <img src="../assets/grafiek.png" alt="grafiek">
          </div>
      </div>
</template>

<script>
import {myFunctions} from '../main.js';

export default {
  data: function() {
    return {
      value: 2,
      time : "10 : 00: 00"
    }
  },
  created: function() {
      let documentReference = myFunctions.getDocumentReference('realtime', 'IC_70')
      //console.log(documentReference)
      documentReference.onSnapshot((doc) =>{
        //console.log("Current data: ", doc.data());
        this.value = doc.data().current_value;
        let d = doc.data().last_updated.toDate();
        this.time = this.zeros(d.getHours(),2) + ":" + this.zeros(d.getMinutes(),2) + " " + d.getDate() + "/" + this.zeros( d.getMonth(), 2) + "/" + d.getFullYear()
      });
    },
  methods:{
    zeros(num, size){
      var s = num+"";
      while (s.length < size) s = "0" + s;
      return s;
    }
  }
}
</script>

<style scoped>

.card{
  max-height: 450px;
  margin: 15px;
  padding: 49px;
  background-color: var(--color-neutral-xxxx-light);
  border-radius: 8px;
  box-shadow: 0 2px 0 rgba(0,0,0,.2);
}
.topbar{
  display: flex;
  justify-content: space-between;
}

.update{
  text-align: right;
  font-size: 13px;
  margin: 0;
}

.grafiek{
  padding-top: 32px;
  background-color: inherit;
}

h1, h2, p{
  margin-bottom: 16px;
}

h1{
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  color: var(--color-neutral-xxxx-dark);
  background-color: inherit;
}

h2{
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  color: var(--color-primary);
  background-color: inherit;
  display: inline;
}

p{
  background-color: inherit;
  font-size: 18px;
  font-weight: 400;
  line-height: 30px;
  display: inline;
  margin-right: 16px;
  color: var(--color-neutral-xxxx-dark)
}

@media (max-width: 992px) {
  .grafiek img{
    width: 90%;
  }
  h1, h2{
    font-size: 18px;
  }
  p {
    font-size: 16px;
  }
  .update{
  font-size: 11px;
}


}
@media (max-width: 576px) {
  .side_bar {
    width: 100vw;
    height: 100vh;
  }
}

</style>
