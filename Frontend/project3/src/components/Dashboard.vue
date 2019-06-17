<template>
  <div class="page">
    <div class="side_bar">
      <div class="side_bar_logo">
        <svg class="logo" viewBox="0 0 512 512" width="100%" height="100%">
          <path
            d="M256 403.3c-115 0-208.7-66.2-208.7-147.3S141 108.7 256 108.7 464.7 174.9 464.7 256 371 403.3 256 403.3m0-311.9C116.6 91.4 4 164.6 4 256s112.6 164.6 252 164.6 252-74 252-164.6S395.4 91.4 256 91.4"
            xmlns="http://www.w3.org/2000/svg"
          ></path>
          <path
            d="M267 342.6h-27.6c-8.7 0-13.4-3.9-13.4-11v-63c0-3.9 1.6-5.5 5.5-5.5H267c22.3 0 40.5 17.9 40.9 40.2.3 21.5-16.9 39.1-38.4 39.4-.8 0-1.6 0-2.5-.1M226.1 182c0-7.1 4.7-11 13.4-11h18.1c18.7-.8 34.6 13.7 35.4 32.4v1.5c-.3 19.3-16.1 34.8-35.4 34.6h-26c-3.9 0-5.5-1.6-5.5-5.5v-52zm111 70.1c-5.5-2.4-5.5-3.2 0-6.3 14.1-8.7 22.5-24.3 22-40.9 0-30.7-40.9-61.4-106.3-61.4-37.8-.2-74.5 12-104.7 34.6-5.5 4.7-4.7 7.1-3.1 8.7l9.5 11c3.1 3.2 4.7 2.4 6.3.8 7.1-5.5 7.9-2.4 7.9 3.9v108.7c0 6.3-.8 9.5-7.9 3.9-1.6-1.6-3.1-2.4-6.3.8l-10.2 11.8c-1.6 2.4-3.1 4.7 3.2 8.7 31.6 21.6 68.8 33.4 107.1 33.9 73.2 0 118.9-30.7 118.9-71.7.6-27.6-22.2-41-36.4-46.5"
            xmlns="http://www.w3.org/2000/svg"
          ></path>
        </svg>

        <svg
          width="24"
          height="24"
          viewBox="0 0 24 24"
          class="logo logo_settings"
          @click="showAdminPage"
        >
          <path fill="none" d="M0 0h24v24H0V0z" />
          <path
            d="M19.43 12.98c.04-.32.07-.64.07-.98s-.03-.66-.07-.98l2.11-1.65c.19-.15.24-.42.12-.64l-2-3.46c-.12-.22-.39-.3-.61-.22l-2.49 1c-.52-.4-1.08-.73-1.69-.98l-.38-2.65C14.46 2.18 14.25 2 14 2h-4c-.25 0-.46.18-.49.42l-.38 2.65c-.61.25-1.17.59-1.69.98l-2.49-1c-.23-.09-.49 0-.61.22l-2 3.46c-.13.22-.07.49.12.64l2.11 1.65c-.04.32-.07.65-.07.98s.03.66.07.98l-2.11 1.65c-.19.15-.24.42-.12.64l2 3.46c.12.22.39.3.61.22l2.49-1c.52.4 1.08.73 1.69.98l.38 2.65c.03.24.24.42.49.42h4c.25 0 .46-.18.49-.42l.38-2.65c.61-.25 1.17-.59 1.69-.98l2.49 1c.23.09.49 0 .61-.22l2-3.46c.12-.22.07-.49-.12-.64l-2.11-1.65zM12 15.5c-1.93 0-3.5-1.57-3.5-3.5s1.57-3.5 3.5-3.5 3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"
          />
        </svg>
      </div>

      <div class="side_bar_input">
        <Datalist v-model="datalist" label="Trein" :ids="allTrainIds" />
        <div>
          <p class="subtitle">Van</p>
          <div class="date_time">
            <Input
              v-model="fromDate"
              class="date_time_item"
              label="Datum:"
              type="date"
              :text-value="fromDate"
            />
            <Input
              v-model="fromTime"
              class="date_time_item"
              label="Tijd:"
              type="time"
              :text-value="fromTime"
            />
          </div>
        </div>
        <div>
          <p class="subtitle">Tot</p>
          <div class="date_time">
            <Input
              v-model="untilDate"
              class="date_time_item"
              label="Datum:"
              type="date"
              :text-value="untilDate"
            />

            <Input
              v-model="untilTime"
              class="date_time_item"
              label="Tijd:"
              type="time"
              :text-value="untilTime"
            />
          </div>
        </div>
        <Button class="button" text="Zoek" @click.native="search" />
      </div>

      <div class="side_bar_dots">
        <div class="dots"></div>
      </div>
    </div>

    <div class="main">
      <Button class="button" text="Logout" @click.native="Logout" />
      <div class="container">
        <div class="cards">
          <Card
            v-for="trainId in trainIds"
            :key="trainId"
            :train-id="trainId"
            :random-id="randomId"
            :d-start="dStart"
            :d-end="dEnd"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Card from './Card.vue'
import Button from './Button.vue'
import Input from './Input.vue'
import Datalist from './Datalist.vue'

export default {
  name: 'Dashboard',
  components: {
    Card,
    Button,
    Input,
    Datalist
  },
  data: function() {
    let d = new Date()
    d.setHours(d.getHours() - 1)
    return {
      allTrainIds: [],
      trainIds: [],
      randomId: 0,
      dStart: d,
      dEnd: new Date(),
      fromDate: '',
      fromTime: '',
      untilDate: '',
      untilTime: '',
      datalist: ''
    }
  },
  created: async function() {
    let today = new Date()
    let h = this.zeros(today.getHours(), 2)
    let m = this.zeros(today.getMinutes(), 2)

    this.untilDate = this.formatDate(today)
    this.fromDate = this.formatDate(today)

    let time = h + ':' + m
    this.untilTime = time

    time = h - 1
    if (time < 0) {
      time = '23'
      let yesterday = today
      yesterday.setDate(yesterday.getDate() - 1)
      this.fromDate = this.formatDate(yesterday)
    }
    time = this.zeros(time, 2)
    time += ':' + m

    this.fromTime = time

    let data = await this.$store.dispatch(
      'firestore/getCollectionDocs',
      'realtime'
    )
    for (let i = 0; i < data.docs.length; i++) {
      this.allTrainIds.push(data.docs[i].id)
      this.trainIds = this.allTrainIds
    }
  },
  methods: {
    zeros(num, size) {
      var s = num + ''
      while (s.length < size) s = '0' + s
      return s
    },
    formatDate(datum) {
      let dd = String(datum.getDate()).padStart(2, '0')
      let mm = String(datum.getMonth() + 1).padStart(2, '0') //January is 0! reason + 1
      let yyyy = datum.getFullYear()
      return yyyy + '-' + mm + '-' + dd
    },
    Logout() {
      this.$store.dispatch('authentication/logout')
    },
    search: function() {
      this.$store.dispatch('firestore/setFilteredState', true)
      this.randomId = this.randomId + 1
      this.dStart = new Date(this.fromDate + ' ' + this.fromTime)
      this.dEnd = new Date(this.untilDate + ' ' + this.untilTime)
      if (this.datalist != '') {
        this.trainIds = [this.datalist]
      } else {
        this.trainIds = this.allTrainIds
      }
    },
    showAdminPage() {
      this.$store.dispatch('authentication/setAdminState', true)
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

.logo_settings {
  width: 40px !important;
  height: 40px !important;
}
.side_bar_input {
  margin: 1em 0;
}
.border_color {
  border-color: var(--color-error-message);
}
.subtitle {
  color: var(--color-primary-x-light);
  margin-top: 23px;
}
.date_time {
  display: flex;
  justify-content: space-between;
}
.date_time_item {
  width: calc(50% - 8px);
}
.date_time .date_time_item {
  margin: 0;
}

@media (max-width: 768px) {
  .date_time {
    justify-content: flex-start;
  }
  .date_time_item {
    width: 25%;
  }
  .date_time .date_time_item {
    margin-right: 16px;
  }
}
@media (max-width: 576px) {
  .date_time {
    display: flex;
    justify-content: space-between;
  }
  .date_time_item {
    width: calc(50% - 8px);
  }
  .date_time .date_time_item {
    margin: 0;
  }
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
.logo {
  width: 65px;
  height: 60px;
  fill: var(--color-neutral-xxxx-light);
}

.button {
  margin-top: 13%;
}
@media (max-width: 768px) {
  .button {
    width: calc(50% + 16px);
  }
}

.main {
  width: calc(100% - 420px);
  margin-left: 420px;
}
@media (max-width: 768px) {
  .main {
    width: 100vw;
    margin: 0%;
  }
}

.top-bar {
  padding: 12px;
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
@media (max-width: 768px) {
  .main .button {
    margin: 50px;
    background-color: var(--color-neutral-xxxx-light);
    color: var(--color-primary);
  }
  .main .button:hover,
  .main.button:active {
    box-shadow: var(--box-shadow_hover);
    color: var(--color-primary-xx-dark);
  }
}
@media (max-width: 576px) {
  .main .button {
    margin: 35px;
  }
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
.update {
  display: flex;
  justify-content: flex-end;
  padding: 12px;
}

@media (max-width: 1200px) {
  .card {
    padding: 30px;
    width: calc(100% - 50px);
  }
}
@media (max-width: 768px) {
  .card {
    padding: 8px;
    width: 100%;
  }
}
</style>
