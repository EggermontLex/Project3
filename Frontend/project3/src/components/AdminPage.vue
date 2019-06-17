<template>
  <div class="page">
    <div class="main">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        class="logo"
        @click="showDashboard"
      >
        <path fill="none" d="M0 0h24v24H0V0z" />
        <path
          d="M10 19v-5h4v5c0 .55.45 1 1 1h3c.55 0 1-.45 1-1v-7h1.7c.46 0 .68-.57.33-.87L12.67 3.6c-.38-.34-.96-.34-1.34 0l-8.36 7.53c-.34.3-.13.87.33.87H5v7c0 .55.45 1 1 1h3c.55 0 1-.45 1-1z"
        />
      </svg>
      <Button class="button" text="Logout" @click.native="Logout" />
      <div class="container">
        <div class="cards">
          <CardAdmin :devises="devises" :all-train-ids="allTrainIds" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Button from './Button.vue'
import CardAdmin from './CardAdmin.vue'

export default {
  name: 'AdminPage',
  components: {
    Button,
    CardAdmin
  },
  data: function() {
    return {
      allTrainIds: [],
      isError: false,
      devises: []
    }
  },
  created: async function() {
    this.devises = await fetch(
      'https://europe-west1-project3-ml6.cloudfunctions.net/list_devices'
    ).then(function(response) {
      //console.log(response.json())
      return response.json()
    })
    for (let devise = 0; devise < this.devises.length; devise++) {
      this.allTrainIds.push(this.devises[devise].train)
      this.devises[devise].isNew = false
      if (this.devises[devise].train == '') {
        this.devises[devise].isNew = true
      }
    }
    let data = await this.$store.dispatch(
      'firestore/getCollectionDocs',
      'realtime'
    )
    for (let i = 0; i < data.docs.length; i++) {
      //console.log('Data',)
      this.allTrainIds.push(data.docs[i].id)
    }
    this.allTrainIds = [...new Set(this.allTrainIds)]
    //console.log(this.allTrainIds)
  },
  methods: {
    showDashboard() {
      this.$store.dispatch('authentication/setAdminState', false)
    }
  }
}
</script>

<style scoped>
.page {
  width: 100vw;
  height: 100vh;
}
.side_bar {
  position: fixed;
  padding: 35px;
  width: 420px;
  height: 100vh;
  background-color: var(--color-primary);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
@media (max-width: 768px) {
  .side_bar {
    width: 100vw;
    height: calc(100vh - 50px);
    position: static;
    padding: 50px;
  }
}

@media (max-width: 576px) {
  .side_bar {
    padding: 35px;
  }
}
.side_bar_logo {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;
}
@media (max-width: 576px) {
  .side_bar_logo {
    align-items: flex-start;
    flex-direction: column;
  }
}

.side_bar_input {
  margin: 1em 0;
}

.error_message {
  background-color: var(--color-neutral-xxxx-light);
  padding: 8px;
  margin-bottom: 16px;
  box-shadow: var(box-shadow);
  text-align: center;
}
.error_message_text {
  color: var(--color-error-message);
}
.logo {
  fill: var(--color-primary);
  width: 65px;
  height: 60px;
  margin: 12px;
}
.button {
  margin-top: 13%;
}
.dots {
  background-image: url('data:image/svg+xml;utf8,<svg version="1.1" id="Layer_1" focusable="false" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 1345.9 27" style="enable-background:new 0 0 1345.9 27;" xml:space="preserve"><circle fill="%23fff" cx="1042.9" cy="3" r="3"/><circle fill="%23fff" cx="1062.9" cy="3" r="3"/><circle fill="%23fff" cx="1082.9" cy="3" r="3"/><circle fill="%23fff" cx="1102.9" cy="3" r="3"/><circle fill="%23fff" cx="1122.9" cy="3" r="3"/><circle fill="%23fff" cx="1142.9" cy="3" r="3"/><circle fill="%23fff" cx="1162.9" cy="3" r="3"/><circle fill="%23fff" cx="1182.9" cy="3" r="3"/><circle fill="%23fff" cx="1202.9" cy="3" r="3"/><circle fill="%23fff" cx="1222.9" cy="3" r="3"/><circle fill="%23fff" cx="1242.9" cy="3" r="3"/><circle fill="%23fff" cx="1262.9" cy="3" r="3"/><circle fill="%23fff" cx="1282.9" cy="3" r="3"/><circle fill="%23fff" cx="1302.9" cy="3" r="3"/><circle fill="%23fff" cx="1322.9" cy="3" r="3"/><circle fill="%23fff" cx="1342.9" cy="3" r="3"/><circle fill="%23fff" cx="742.9" cy="3" r="3"/><circle fill="%23fff" cx="762.9" cy="3" r="3"/><circle fill="%23fff" cx="782.9" cy="3" r="3"/><circle fill="%23fff" cx="802.9" cy="3" r="3"/><circle fill="%23fff" cx="822.9" cy="3" r="3"/><circle fill="%23fff" cx="842.9" cy="3" r="3"/><circle fill="%23fff" cx="862.9" cy="3" r="3"/><circle fill="%23fff" cx="882.9" cy="3" r="3"/><circle fill="%23fff" cx="902.9" cy="3" r="3"/><circle fill="%23fff" cx="922.9" cy="3" r="3"/><circle fill="%23fff" cx="942.9" cy="3" r="3"/><circle fill="%23fff" cx="962.9" cy="3" r="3"/><circle fill="%23fff" cx="982.9" cy="3" r="3"/><circle fill="%23fff" cx="1002.9" cy="3" r="3"/><circle fill="%23fff" cx="1022.9" cy="3" r="3"/><path fill="%23fff" d="M1301.1,13.7c0,3.3-2.2,8.3-8.2,8.3c-5.3,0-8.2-5-8.2-8.6V13h-4.8v0.4c0,6.6,4.1,13.6,13,13.6c8.9,0,13-6.9,13-13.3v-0.4 h-4.8V13.7z"/><circle fill="%23fff" cx="602.9" cy="3" r="3"/><circle fill="%23fff" cx="622.9" cy="3" r="3"/><circle fill="%23fff" cx="642.9" cy="3" r="3"/><circle fill="%23fff" cx="662.9" cy="3" r="3"/><circle fill="%23fff" cx="682.9" cy="3" r="3"/><circle fill="%23fff" cx="702.9" cy="3" r="3"/><path fill="%23fff" d="M724.6,0.5c-1.4-0.9-3.2-0.6-4.2,0.8c-0.9,1.4-0.6,3.2,0.8,4.2c1,0.7,2.3,0.7,3.4,0c0.5-0.3,0.9-0.8,1.1-1.3 c0.3-0.7,0.3-1.6,0-2.3C725.5,1.3,725.1,0.8,724.6,0.5z"/><circle fill="%23fff" cx="442.9" cy="3" r="3"/><circle fill="%23fff" cx="462.9" cy="3" r="3"/><circle fill="%23fff" cx="482.9" cy="3" r="3"/><circle fill="%23fff" cx="502.9" cy="3" r="3"/><circle fill="%23fff" cx="522.9" cy="3" r="3"/><circle fill="%23fff" cx="542.9" cy="3" r="3"/><circle fill="%23fff" cx="562.9" cy="3" r="3"/><circle fill="%23fff" cx="582.9" cy="3" r="3"/><circle fill="%23fff" cx="302.9" cy="3" r="3"/><circle fill="%23fff" cx="322.9" cy="3" r="3"/><circle fill="%23fff" cx="342.9" cy="3" r="3"/><circle fill="%23fff" cx="362.9" cy="3" r="3"/><circle fill="%23fff" cx="382.9" cy="3" r="3"/><circle fill="%23fff" cx="402.9" cy="3" r="3"/><path fill="%23fff" d="M424.6,0.5c-1.4-0.9-3.2-0.6-4.2,0.8c-0.9,1.4-0.6,3.2,0.8,4.2c1,0.7,2.3,0.7,3.4,0c0.5-0.3,0.9-0.8,1.1-1.3 c0.3-0.7,0.3-1.6,0-2.3C425.5,1.3,425.1,0.8,424.6,0.5z"/><circle fill="%23fff" cx="143.1" cy="3" r="3"/><circle fill="%23fff" cx="163.1" cy="3" r="3"/><circle fill="%23fff" cx="183.1" cy="3" r="3"/><circle fill="%23fff" cx="203.1" cy="3" r="3"/><circle fill="%23fff" cx="223.1" cy="3" r="3"/><circle fill="%23fff" cx="243.1" cy="3" r="3"/><circle fill="%23fff" cx="263.1" cy="3" r="3"/><circle fill="%23fff" cx="283.1" cy="3" r="3"/><circle fill="%23fff" cx="3.1" cy="3" r="3"/><circle fill="%23fff" cx="23.1" cy="3" r="3"/><circle fill="%23fff" cx="43.1" cy="3" r="3"/><circle fill="%23fff" cx="63.1" cy="3" r="3"/><circle fill="%23fff" cx="83.1" cy="3" r="3"/><circle fill="%23fff" cx="103.1" cy="3" r="3"/><path fill="%23fff" d="M124.8,0.5c-1.4-0.9-3.2-0.6-4.2,0.8c-0.9,1.4-0.6,3.2,0.8,4.2c1,0.7,2.3,0.7,3.3,0c0.5-0.3,0.9-0.8,1.1-1.3 c0.3-0.7,0.3-1.6,0-2.3C125.7,1.3,125.3,0.8,124.8,0.5z"/></svg>');
  height: 40px;
  background-repeat: no-repeat;
  background-position: 100% 0;
  background-size: auto 27px;
}
@media (max-width: 768px) {
  .dots {
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .main {
    width: 100vw;
    margin: 0%;
  }
}
.main .button {
  margin: 12px;
  background-color: var(--color-primary);
  color: var(--color-neutral-xxxx-light);
  width: 150px;
  position: absolute;
  right: 0;
  top: 0;
}
.main .button:hover,
.main .button:active {
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.2);
  color: var(--color-neutral-xxxx-light);
  background-color: var(--color-primary-x-dark);
}
.container {
  height: 100vh;
  padding-top: 60px;
  display: flex;
  justify-content: space-between;
  flex-direction: column;
}

@media (max-width: 768px) {
  .container {
    padding-top: 0px;
  }
}

.cards {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.card {
  max-width: 950px;
}
</style>
