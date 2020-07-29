$(document).ready(function() {
    $('#celsiusButton').click(function() {
        $("#celsiusTempDiv").show();
        $("#fahrenheitButtonDiv").show();
        $("#celsiusButton").hide();
    });
});

var myVar = setInterval(myTimer, 1000);
var myTemp = setInterval(updateTemp, 5000);

function myTimer() {
  var d = new Date();
  document.getElementById("currentTime").innerHTML = d.toLocaleTimeString();
}


url = "/api/status"

async function updateTemp() {
  fetch(url)
    .then((response) => {
	return response.json();
    }).then((data) => {
	document.getElementById("tempInC").innerHTML = JSON.stringify(data.temp);
     });
}

