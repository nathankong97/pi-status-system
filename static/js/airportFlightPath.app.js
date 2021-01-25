var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport-input'));
var url = "/api/v1/airport_flightPath/" + airport;

Plotly.d3.json(url, function(err, data) {
    var arrayData = [];
    var count = data.count;
    var startLongitude = data.start_lng;
    var endLongitude = data.end_lng;
    var startLat = data.start_lat;
    var endLat = data.end_lat;
    var maxCount = data.max_count;

    for ( var i = 0 ; i < count.length; i++ ) {
        var opacityValue = count[i]/maxCount;
        var result = {
            type: 'scattermapbox',
            lon: [ startLongitude[i] , endLongitude[i] ],
            lat: [ startLat[i] , endLat[i] ],
            hovertext: String(count[i]),
            mode: 'lines',
            marker: {
                symbol: "circle",
                size: 12
            },
            line: {
                width: 1,
                color: 'red'
            },
            opacity: opacityValue
        };
        arrayData.push(result);
    }

    var layout = {
            showlegend: false,
			dragmode: "zoom",
			mapbox: { style: "open-street-map", center: { lat: startLat[0], lon: startLongitude[0] }, zoom: 3 },
			margin: { r: 0, t: 0, b: 0, l: 0 }
		};

    Plotly.newPlot("flight-path", arrayData, layout, {showLink: false});
});