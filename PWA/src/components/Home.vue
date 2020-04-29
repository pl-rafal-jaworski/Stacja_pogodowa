<template>
  <div>
    <h1 class="headline">Aktualne dane</h1>

    <div class="blocks-container">
      <div class="block">
        <div class="row">
            <tempEmojiAktualnie></tempEmojiAktualnie>
          <div class="weather-temp">
            <tempAktualna></tempAktualna>
          </div>
        </div>
        <div class="row">
          <div class="summary-title">
            <tempDescAktualnie></tempDescAktualnie>
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
            <cisnienieAktualne></cisnienieAktualne>
          </div>
          <div class="weather-pm">
            <pmAktualne></pmAktualne>
          </div>
        </div>

        <div class="row">
            <div class="timestamp">
              <timestampLast></timestampLast>
            </div>
            </div>
        </div>
      </div>
    </div>
  </div>


</template>

<script>
</script>
