import Vue from 'vue';
const axios = require('axios').default;

var temp =  new Vue({

});

var tempAktualna = Vue.component('tempAktualna',{
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
  template: '<a>{{temp.temp}}</a>',
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
  template: '<a>{{cisnienie.cisnienie}}</a>',
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
