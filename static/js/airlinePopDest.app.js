

function getAirlineAirportResult() {
    var iata = document.getElementById("airline").value;
    var url = "/api/v1/airline/pop_destination/" + iata.toUpperCase();
    fetch(url)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
       $('#AirportHubTable').DataTable({
            "lengthChange": true,
            "info": true,
            "autoWidth": false,
            "bDestroy": true,
            "bSort": false,
            "data": data,
            "columns": [
                { "data": "name"},
                { "data": "iata" }
            ]
        });
    });
}