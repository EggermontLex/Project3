<template>
  <div class="card">
    <div class="textarea">
      <div class="topbar">
        <h1>{{ trainId }}</h1>
        <p class="update">
          Laatst geüpdate:
          <b class="update_text">{{ time }}</b>
        </p>
      </div>
      <p>Aantal mensen binnen:</p>
      <h2>{{ value }}</h2>
    </div>
    <div class="grafiek">
      <apexchart
        ref="realtimeChart"
        type="area"
        height="350"
        :options="chartOptions"
        :series="series"
      />
    </div>
  </div>
</template>

<script>
var _ = require('lodash')
var moment = require('moment')
import { mapState } from 'vuex'

export default {
  props: {
    trainId: {
      type: String,
      default: ''
    },
    dStart: {
      type: Date,
      default: () => {
        let d = new Date()
        d.setHours(d.getHours() - 1)
        return d
      }
    },
    dEnd: {
      type: Date,
      default: () => new Date()
    },
    randomId: {
      type: Number,
      default: 0
    }
  },
  data: function() {
    return {
      data: [],
      value: 0,
      time: '00:00:00',
      series: [
        {
          name: 'Personen',
          data: []
        }
      ],
      chartOptions: {
        chart: {
          height: 350,
          zoom: {
            enabled: false
          },
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          enabled: false
        },
        stroke: {
          curve: 'smooth'
        },
        colors: ['#006AB3'],
        grid: {
          row: {
            colors: ['#F1F5F5', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
          }
        },
        xaxis: {
          type: 'datetime'
        },
        tooltip: {
          x: {
            format: 'dd/MM/yyyy hh:mm:ss'
          }
        }
      }
    }
  },
  computed: {
    ...mapState({
      isFiltered: state => state.firestore.isFiltered
    })
  },
  watch: {
    async randomId() {
      this.data = await this.getHistoryData()
      this.$refs.realtimeChart.updateSeries([
        {
          data: this.data
        }
      ])
    }
  },
  created: async function() {
    let documentReference = await this.$store.dispatch(
      'firestore/getDocumentReference',
      { collection: 'realtime', document: this.$props.trainId }
    )
    documentReference.onSnapshot(doc => {
      this.value = doc.data().current_value
      this.time = this.displayTime(doc.data().last_updated.toDate())
      if (!this.isFiltered) {
        this.data.push({
          x: moment.unix(doc.data().last_updated.seconds).toString(),
          y: this.value
        })
        this.$refs.realtimeChart.updateSeries([
          {
            data: this.data
          }
        ])
      }
    })
    this.data = await this.getHistoryData()
    this.$refs.realtimeChart.updateSeries([
      {
        data: this.data
      }
    ])
  },
  methods: {
    async getHistoryData() {
      let historyData = []
      let groupBy = this.getGroupParameters(this.dStart, this.dEnd)
      let data = await this.$store.dispatch('firestore/getTrainHistory', {
        trainId: this.$props.trainId,
        startTime: this.dStart,
        endTime: this.dEnd
      })
      let groupedResults = _.groupBy(data.docs, result =>
        moment.unix(result.data().timestamp.seconds).startOf(groupBy)
      )
      _.forEach(groupedResults, (n, key) =>
        historyData.push({
          x: key,
          y: Math.round(_.meanBy(n, k => k.data().value))
        })
      )
      return historyData
    },
    getGroupParameters(dStart, dEnd) {
      let start = moment(dStart)
      let end = moment(dEnd)
      let years = end.diff(start, 'years')
      let months = end.diff(start, 'months')
      let weeks = end.diff(start, 'weeks')
      let days = end.diff(start, 'days')
      let minutes = end.diff(start, 'minutes')
      if (years < 1) {
        if (months < 1) {
          if (weeks < 1) {
            if (days < 1) {
              if (minutes < 30) {
                return 'second'
              }
              return 'minute'
            }
            return 'hour'
          }
          return 'day'
        }
        return 'day'
      }
      return 'month'
    },
    zeros(num, size) {
      var s = num + ''
      while (s.length < size) s = '0' + s
      return s
    },
    displayTime(d) {
      return (
        this.zeros(d.getHours(), 2) +
        ':' +
        this.zeros(d.getMinutes(), 2) +
        ' ' +
        d.getDate() +
        '/' +
        this.zeros(d.getMonth() + 1, 2) +
        '/' +
        d.getFullYear()
      )
    }
  }
}
</script>

<style scoped>
.card {
  margin: 15px;
  width: 70%;
  padding: 49px;
  background-color: var(--color-neutral-xxxx-light);
  border-radius: 8px;
  box-shadow: 0 2px 0 rgba(0, 0, 0, 0.2);
}
.topbar {
  display: flex;
  justify-content: space-between;
}

.update {
  text-align: right;
  font-size: 13px;
  margin: 0;
}

.grafiek {
  padding-top: 32px;
  background-color: inherit;
}

h1,
h2,
p {
  margin-bottom: 16px;
}

h1 {
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  color: var(--color-neutral-xxxx-dark);
  background-color: inherit;
}

h2 {
  font-size: 22px;
  font-weight: 700;
  line-height: 30px;
  color: var(--color-primary);
  background-color: inherit;
  display: inline;
}

p {
  background-color: inherit;
  font-size: 18px;
  font-weight: 400;
  line-height: 30px;
  display: inline;
  margin-right: 8px;
  color: var(--color-neutral-xxxx-dark);
}

@media (max-width: 992px) {
  .grafiek img {
    width: 90%;
  }
  h1,
  h2 {
    font-size: 18px;
  }
  p {
    font-size: 16px;
  }
  .update {
    font-size: 11px;
  }
}

@media (max-width: 768px) {
  .textarea {
    margin: 24px 24px 0px;
  }
}

@media (max-width: 576px) {
  .side_bar {
    width: 100vw;
    height: 100vh;
  }
}
</style>
