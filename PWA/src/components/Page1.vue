<template>
  <div>
    <h1 class="headline">Dane historyczne</h1>

    <div class="blocks-container" v-for="i in pastInfo">
      <div class="block" >

        <div class="row">
          <div class="weather-logo">
            {{i.emoji}}
          </div>
          <div class="weather-temp">
            {{i.temp}}°C
          </div>
        </div>
        <div class="row">
          <div class="summary-title">
            {{i.description}}
          </div>
        </div>
        <div class="row-headline">
          <div class="weather-pressure-headline">
            Ćiśnienie
          </div>
          <div class="weather-pm-headline">
            Stężenie PM2.5
          </div>
        </div>
        <div class="row">
          <div class="weather-pressure">
            {{i.cisnienie}}hPa
          </div>
          <div class="weather-pm">
            {{i.pm}}
          </div>
        </div>


        <div class="row">
            <div class="timestamp">
              {{i.timestamp}}
            </div>
        </div>
      </div>
    </div>
  </div>


</template>
<script>
  export default {
    data: function() {
           return  {
             pastInfo: []
           }
      },
      mounted () {
      this.$http.get('http://0.0.0.0:5002/PastData')
      .then((result) => {
        this.pastInfo = result.data
      })
      },
  }


</script>
