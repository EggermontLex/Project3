<template>

      <div class="card">
          <div class="textarea">
            <div class="topbar">
              <h1>{{trainId}}</h1>
              <p class="update">Laatst geüpdate: <b class="update_text">{{ time }}</b></p>
            </div>
            <p>Aantal mensen binnen:</p>
            <h2>{{value}}</h2>
          </div>
          
          <div class="grafiek">
            <!--<img src="../assets/grafiek.png" alt="grafiek">-->
            <apexchart type=area height=350 :options="chartOptions" :series="series" />
          </div>
      </div>
</template>

<script>
import {myFunctions} from '../main.js';

export default {
  data: function() {
    return {
      value: 2,
      time : "10 : 00: 00",
      series: [],
        chartOptions: {
          chart: {
                height: 350,
                zoom: {
                    enabled: false
                }
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            
            grid: {
                row: {
                    colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                    opacity: 0.5
                },
            },
            xaxis: {
                categories: [],
            }
        }
    }
  },
  props: {
    trainId:String
  },
  created: async function() {
      let documentReference = myFunctions.getDocumentReference('realtime', this.$props.trainId)
      documentReference.onSnapshot((doc) =>{
        //console.log("Current data: ", doc.data());
        this.value = doc.data().current_value;
        let d = doc.data().last_updated.toDate();
        this.time = this.zeros(d.getHours(),2) + ":" + this.zeros(d.getMinutes(),2) + " " + d.getDate() + "/" + this.zeros( d.getMonth(), 2) + "/" + d.getFullYear()
      });

      let result = [{
            name: "People",
            data: []
        }];
      let data = await myFunctions.getTrainHistory("history", this.$props.trainId)
      //console.log(data.docs[0].data().value)
      for(let i= 0; i< data.docs.length; i++){
        result[0].data.push(data.docs[i].data().value)
      }
      this.series = result
      
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
  margin: 15px;
  width: 70%;
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
  margin-right: 8px;
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

@media (max-width: 768px) {
  .textarea{
    margin:24px 24px 0px;
  }
}

@media (max-width: 576px) {
  .side_bar {
    width: 100vw;
    height: 100vh;
  }
}

</style>
