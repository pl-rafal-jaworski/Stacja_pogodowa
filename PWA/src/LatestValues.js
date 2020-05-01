import Vue from 'vue';
const axios = require('axios').default;

Vue.component('tempAktualna',{
  data: function() {
         return  {
           temp: "N/A"
         }
    },
    mounted () {
      axios
        .get('http://192.168.1.106:5002/NewestTemp')
        .then(response => (this.temp = response.data))
    },
  template: '<a>{{temp.temp}}°C</a>',
})

Vue.component('cisnienieAktualne',{
  data: function() {
         return  {
           cisnienie: "N/A"
         }
    },
    mounted () {
      axios
        .get('http://192.168.1.106:5002/NewestPressure')
        .then(response => (this.cisnienie = response.data))
    },
  template: '<a>{{cisnienie.cisnienie}}hPa</a>',
})

Vue.component('pmAktualne',{
  data: function() {
         return  {
           pm: "N/A"
         }
    },
    mounted () {
      axios
        .get('http://192.168.1.106:5002/NewestPM')
        .then(response => (this.pm = response.data))
    },
  template: '<a>{{pm.pm}}</a>',
})

Vue.component('timestampLast',{
  data: function() {
         return  {
           timestamp: "N/A"
         }
    },
    mounted () {
      axios
        .get('http://192.168.1.106:5002/NewestTimestamp')
        .then(response => (this.timestamp = response.data))
    },
  template: '<a>{{timestamp.timestamp}}</a>',
})

Vue.component('tempDescAktualnie',{
  data: function() {
         return  {
           tempDesc: "N/A"
         }
    },
    mounted () {
      axios
        .get('http://192.168.1.106:5002/NewestTempDesc')
        .then(response => (this.tempDesc = response.data))
    },
  template: '<a>{{tempDesc.desc}}</a>',
})

Vue.component('tempEmojiAktualnie',{
  data: function() {
         return  {
           tempEmoji: "N/A"
         }
    },
    mounted () {
      axios
        .get('http://192.168.1.106:5002/NewestTempDesc')
        .then(response => (this.tempEmoji = response.data))
    },
  template: '<div class="weather-logo">{{tempEmoji.emoji}}</div>',
})
