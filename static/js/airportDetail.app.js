var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport-input'));
var url = '/api/v1/airport_detail/' + airport;

fetch(url)
  .then((response) => {
    return response.json();
  })
  .then((myJson) => {
      var data = myJson.result.response.airport.pluginData.details;
      var icao = data.code.icao;
      var lat = data.position.latitude;
      var lng = data.position.longitude;
      var elv = data.position.elevation;
      var elv_in_m = Math.round(elv / 3.281);
      document.getElementById("airport-name").innerHTML = data.name;
      if (data.airportImages !== null) {
          document.getElementById("airport-img").src = data.airportImages.large[0].src;
      } else {
          document.getElementById("airport-img").src = "";
      }
      document.getElementById("airport-location").innerHTML = data.position.region.city + ", "
          + data.position.country.name + " (" + airport + "/" + icao + ")";
      document.getElementById("lat").innerHTML = lat + " °";
      document.getElementById("lng").innerHTML = lng + " °";
      document.getElementById("elv").innerHTML = elv + " ft/" + elv_in_m + " m";
      var map_link = "//www.openstreetmap.org/export/embed.html?bbox="
          + String(lng - 0.015) + "," + String(lat - 0.015) + "," + String(lng + 0.015) +
          "," + String(lat + 0.015) +
          "&marker=" + lng + "," + lat + "&amp;layers=ND";
      document.getElementById("airport-map").src = map_link;
      document.getElementById("main-site").href = data.url.homepage;
      document.getElementById("wiki-site").href = data.url.wikipedia;

      var runways = myJson.result.response.airport.pluginData.runways;
      document.getElementById("runways").innerHTML = processRunway(runways);
    });

function processRunway(data) {
    var i;
    var s = '<dl class="row">'
    s += '<dt class="col-sm-6">Direction</dt><dt class="col-sm-6">Length/Surface</dt>';
    for (i = 0; i < data.length / 2 ; i++) {
        var num = data[i].name.match(/\d/g);
        num = parseInt(num.join(""));
        var opposite_num = Math.abs(18 + num);
        if (data[i].name.includes("L")) {
            var opposite_let = "R";
        } else if (data[i].name.includes("C")) {
            var opposite_let = "C";
        } else if (data[i].name.includes("R")) {
            var opposite_let = "L";
        } else {
            var opposite_let = "";
        }
        var final_name = data[i].name + "/" + String(opposite_num) + opposite_let;
        s += '<dt class="col-sm-6">' + final_name + '</dt>';
        s += '<dd class="col-sm-6">' + data[i].length.m + "m / " + data[i].surface.name + '</dd>';
    }
    s += '</dl>';
    return s
}
