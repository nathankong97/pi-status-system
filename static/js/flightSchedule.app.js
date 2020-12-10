var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport'));
var airportQueryType = String(params.get('optradio'));

console.log(airport);
console.log(airportQueryType);

var url = "/api/v1/flightSchedule/" + airport + "/" + airportQueryType;

fetch(url)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log(data);
        document.getElementById("totalFlights").innerHTML = data.totalFlights - data.canceledCounts;
        document.getElementById("internationalFlights").innerHTML = data.internationalDomestic.international;
        document.getElementById("passengerTraffic").innerHTML = data.passengerTraffic;
        cancelFlight(data.canceledCounts);
        farthestDestination(data.topDistance);
        var rate = Math.round((data.totalFlights - data.canceledCounts) / data.totalFlights * 100).toFixed(1);
        onTimeRate(rate);
        destinationMap(data.destinationWithLocation);
    });

function cancelFlight(count) {
    if (count < 10) {
        document.getElementById("cancelFlights").innerHTML = count;
    } else if (count < 20 && count >= 10) {
        document.getElementById("cancelFlights").innerHTML = "<font color='orange'>" + count + "</font>";
    } else {
        document.getElementById("cancelFlights").innerHTML = "<font color='red'>" + count + "</font>";
    }
}

function farthestDestination(data) { //this is for inside of the table/body
    var content = "";
    for (var i = 0; i < data.length; i++) {
        var item = data[i];
        content += "<tr><td>" + item.city + "</td>";
        content += "<td>" + item.country + "</td>";
        content += "<td>" + item.name + "</td>";
        content += "<td>" + item.distance + "</td></tr>";
    }
    document.getElementById("destinationTable").innerHTML = content;
}

function onTimeRate(data) {
    if (data >= 80) {
        document.getElementById("ontimerate").innerHTML = String(data) + " <small>%</small>";
    } else if (data < 80 && data >= 60) { 
        document.getElementById("ontimerate").innerHTML = "<font color='#ffcc00'>" + String(data) + " <small>%</small></font>";
    } else {
        document.getElementById("ontimerate").innerHTML = "<font color='#f32013'>" + String(data) + " <small>%</small></font>";
    }
}

function destinationMap(data) {
    $(function () {
        $('#worldMap').vectorMap({
            map: 'world_mill',
            scaleColors: ['#C8EEFF', '#0071A4'],
            normalizeFunction: 'polynomial',
            hoverOpacity: 0.7,
            hoverColor: false,
            markerStyle: {
                initial: {
                    fill: '#F8E23B',
                    stroke: '#383f47',
                    r: 3
                }
            },
            backgroundColor: '#383f47',
            markers: data,
        });
    });
}