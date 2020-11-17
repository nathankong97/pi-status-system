var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport'));
var url = "/api/v1/airport/" + airport

fetch(url)
  .then((response) => {
    return response.json();
  })
  .then((myJson) => {
    document.getElementById("airportCode").innerHTML = "[" + myJson.IATA + "/" + myJson.ICAO + "]";
    document.getElementById("airportName").innerHTML = myJson.Name;
    document.getElementById("airportCity").innerHTML = myJson.City;
    document.getElementById("airportCountry").innerHTML = myJson.Country;
    document.getElementById("googleMapUrl").href = "http://www.google.com/maps/place/" + String(myJson.Latitude) + "," + String(myJson.Longitude);
    //document.getElementById("darkSkyWeather").href = "https://darksky.net/forecast/" + String(myJson.Latitude) + "," + String(myJson.Longitude) + "/ca12/en";
    //var countryCode = String(myJson.countryCode);
    console.log(myJson);
    });