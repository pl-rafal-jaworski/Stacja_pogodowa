let sql = `SELECT DISTINCT Name name FROM playlists
           ORDER BY name`;

db.all(sql, [], (err, rows) => {
  if (err) {
    throw err;
  }
  rows.forEach((row) => {
    console.log(row.name);
  });
});

<template>
  <div>
    <h1 class="headline">Dane historyczne</h1>

    <div class="blocks-container">
      <div class="block">

        <div class="row">
          <div class="weather-logo">
            🌞
          </div>
          <div class="weather-temp">
            20°C
          </div>
        </div>
        <div class="row">
          <div class="summary-title">
            Słonecznie
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
            1010hPa
          </div>
          <div class="weather-pm">
            0.25
          </div>
        </div>


        <div class="row">
            <div class="timestamp">
              20s temu
            </div>
        </div>
      </div>

      <div class="block">
        <div class="row">
          <div class="weather-logo">
            🌧️
          </div>
          <div class="weather-temp">
            19°C
          </div>
        </div>
        <div class="row">
          <div class="summary-title">
            Deszczowo
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
            1013hPa
          </div>
          <div class="weather-pm">
            0.25
          </div>
        </div>


        <div class="row">
            <div class="timestamp">
              1d temu
            </div>
        </div>
      </div>

      <div class="block">

        <div class="row">
          <div class="weather-logo">
            ⛅
          </div>
          <div class="weather-temp">
            17°C
          </div>
        </div>
        <div class="row">
          <div class="summary-title">
            Pochmurno
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
            1010hPa
          </div>
          <div class="weather-pm">
            0.25
          </div>
        </div>


        <div class="row">
            <div class="timestamp">
              2d temu
            </div>
        </div>
      </div>
    </div>
  </div>


</template>
<script>
</script>
