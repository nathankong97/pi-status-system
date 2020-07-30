var url = "/api/v1/test"
var myStatus = setInterval(updateStatus, 5000);
var myTime = setInterval(myTimer, 1000);


function myTimer() {
  var d = new Date();
  document.getElementById("currentTime").innerHTML = d.toLocaleTimeString();
}

async function updateStatus() {
  fetch(url)
    .then((response) => {
	return response.json();
    }).then((data) => {
	    document.getElementById("processor").innerHTML = JSON.stringify(data.processor);
	    document.getElementById("ipAddress").innerHTML = data.ipAddress;
	    document.getElementById("memory").innerHTML = JSON.stringify(data.memory);
	    document.getElementById("uptime").innerHTML = JSON.stringify(data.uptime);
	    document.getElementById("disk_usage").innerHTML = JSON.stringify(data.disk_usage);
	    document.getElementById("cpu_temp").innerHTML = JSON.stringify(data.cpu_temp);
	    document.getElementById("basic_info").innerHTML = data.basic_info;
    });
}