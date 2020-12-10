var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport'));

var url = "/api/v1/weather/" + airport

fetch(url)
  .then((response) => {
    return response.json();
  })
  .then((myJson) => {
    if (myJson.metar === "Not Found") {
        document.getElementById("airportWeather").innerHTML = "Not Aviliable";
    } else {
        var content = myJson.metar + "<br><br>";
        content += '<button type="button" class="btn btn-outline-primary" data-toggle="modal" data-target="#weatherModal">Detail</button>';
        var modalContent = '<table class="table table-hover">';
        modalContent += '<tr><td>Temperature</td><td>' + myJson.temp.celsius + ' °C</td></tr>';
        modalContent += '<tr><td>Condition</td><td>' + myJson.sky.condition.text + '</td></tr>';
        modalContent += '<tr><td>Humidity</td><td>' + myJson.humidity + ' %</td></tr>';
        modalContent += '<tr><td>Pressure</td><td>' + myJson.pressure.hpa + ' hPa</td></tr>';
        modalContent += '<tr><td>Visibility</td><td>' + String(myJson.sky.visibility.mi * 1.6) + ' km</td></tr>';
        modalContent += '<tr><td>Wind Direction</td><td>' + myJson.wind.direction.degree + "° " + myJson.wind.direction.text + '</td></tr>';
        modalContent += '<tr><td>Wind Speed</td><td>' + myJson.wind.speed.kmh + ' km/h</td></tr>';
        modalContent += "</table>";
        document.getElementById("weatherDetail").innerHTML = modalContent;
        document.getElementById("airportWeather").innerHTML = content;
    }
    //console.log(myJson);
    });