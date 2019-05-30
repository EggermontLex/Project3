<template>
    <div class="card">
        <h1>Huidige waarden</h1>
        <p>Aantal mensen:</p>
        <h2>1</h2>
        <div class="grafiek">
        <img src="../assets/grafiek.png" alt="grafiek">
        </div>
    </div>
</template>

<script>
export default {}
</script>

<style scoped>
.card{
  margin: 15px;
  padding: 49px;
  background-color: #FFF !important;
  border-radius: 8px;
  box-shadow: 0 2px 0 rgba(0,0,0,.2);
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
  color: #3A3A3A;
  background-color: inherit;
}

h2{
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  color: #006AB3;
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
}
</style>
