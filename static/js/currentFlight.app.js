var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport'));
var airportQueryType = String(params.get('optradio'));

var url = "/api/v1/currentFlight/" + airport + "/" + airportQueryType;


fetch(url)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        prepareFlightTable(data.flights);
    });


function prepareFlightTable(data) {
    $('#flightTable').DataTable({
        "paging": true,
        "lengthChange": true,
        "searching": true,
        "ordering": true,
        "info": true,
        "autoWidth": false,
        "responsive": true,
        "data": data,
        "columns": [
            { "data": "sched_dep" },
            { "data": "status_detail" },
            { "data": "flight_num" },
            { "data": "dest_city" },    
            { "data": "airline" },
            { "data": "origin_terminal" },
            { "data": "origin_gate" },
            { "data": "aircraft_text" }
        ]
    });
}