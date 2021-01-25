var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport-input'));
var url = "/api/v1/timeSeries/" + airport;

Plotly.d3.json(url, function(err, data) {
    var trace1 = {
      type: "scatter",
      mode: "lines",
      name: 'Departure',
      x: data.origin_time,
      y: data.origin_count,
      line: {color: '#17BECF'}
    }

    var trace2 = {
      type: "scatter",
      mode: "lines",
      name: 'Arrival',
      x: data.origin_time,
      y: data.arrival_count,
      line: {color: '#7F7F7F'}
    }

    var arrayData = [trace1,trace2];

    var layout = {
      title: 'Basic Time Series',
    };

    Plotly.newPlot('flight-time-chart', arrayData, layout);
})