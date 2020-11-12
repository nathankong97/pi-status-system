

var test_url = "/api/v1/test";
var url = "api/v1/status";
var loc_url = "api/v1/location";

var myStatusDev = setInterval(updateStatus, 2000)
var myTime = setInterval(myTimer, 1000);
var myLocation;
fetchPiAwareAddress();



function fetchPiAwareAddress() {
	document.getElementById('pi-aware-address').href= "http://" + window.location.hostname + ":8080";
}

function myTimer() {
  var d = new Date();
  document.getElementById("currentTime").innerHTML = d.toLocaleTimeString();
}

function updateStatus() {
  fetch(url)
    .then((response) => {
	return response.json();
    }).then((data) => {
		document.getElementById("memory-usage-progbar").style.width = String(data["memory"]["use in %"]) + "%";
		document.getElementById("memory-usage-progbar").style.color = "black";
		document.getElementById("memory-usage-progbar").innerHTML = String(data["memory"]["use in %"]) + "%";
		document.getElementById("system-info").innerHTML = data["system_info"];
		document.getElementById("model-name").innerHTML = data["basic_info"]["modelNnum"];
		document.getElementById("cpu-model").innerHTML = data["cpu_info"]["Model name"];
		document.getElementById("cpu-core").innerHTML = data["cpu_info"]["CPU(s)"];
		document.getElementById("mac-address").innerHTML = data["mac_address"];
		document.getElementById("ipv4").innerHTML = data["ip_address"]["ipv4"];
		document.getElementById("ipv6").innerHTML = data["ip_address"]["ipv6"];
		document.getElementById("uptime").innerHTML = uptime_format(data);
		document.getElementById("wifi-name").innerHTML = data["wifi_name"];
		document.getElementById("wifi-device").innerHTML = list_devices(data);
		document.getElementById("wifi-quality").innerHTML = data["wifi_power"]["quality"] + "/70";
		document.getElementById("wifi-signal").innerHTML = data["wifi_power"]["signal"] + " dBm";
		document.getElementById("processor-content").innerHTML = processor_content(data);
		document.getElementById("mem-total").innerHTML = data["memory"]["total size"] + " MB";
		document.getElementById("mem-used").innerHTML = data["memory"]["used"] + " MB";
		document.getElementById("mem-avai").innerHTML = data["memory"]["avail"] + " MB";
		document.getElementById("last-time").innerHTML = data["last_login"];
		document.getElementById("disk-usage-progbar").style.width = data["disk_usage"]["use in %"];
		document.getElementById("disk-usage-progbar").innerHTML = data["disk_usage"]["use in %"];
		document.getElementById("disk-total").innerHTML = data["disk_usage"]["size"];
		document.getElementById("disk-used").innerHTML = data["disk_usage"]["used"];
		document.getElementById("disk-avai").innerHTML = data["disk_usage"]["avail"];
		document.getElementById("temp-progbar").style.width = data["sensor_cpu_temp"]["temp_c"] + "%";
		document.getElementById("temp-progbar").innerHTML = data["sensor_cpu_temp"]["temp_c"] + " °C";
		//document.getElementById("cpu-temp").value = data["sensor_cpu_temp"]["temp_c"];
    });
}

function locationStatus() {
	fetch(loc_url)
	  .then((response) => {
		  }).then((data) => {
			  return response.json();
			  }).then((data) => {
				  
			  });
}


function list_devices(data) {
	var devices = data["devices_on_wifi"];
	var output_code = "<ul class='list-unstyled'>";
	for (i = 0, len = devices.length; i < len; i++) {
		output_code += "<li>" + devices[i] + "</li>";
	}
	output_code += "</ul>";
	return output_code;
}

function uptime_format(data) {
	var time = data["uptime"];
	return time["days"] + " days " + time["hours"] + " hours " + time["minutes"] + " minutes";
}

function processor_content(data) {
	var row = "";
	var content = data["processor"];
	for (var elm in content) {
		row += "<td>" + content[elm] + "</td>";
	}
	return row;
}