

function getFlightNumResult() {
    var flightnum = document.getElementById("airline").value;
    var url = "/api/v1/flight_num/" + flightnum.toUpperCase();
    fetch(url)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
       $('#flightNumTable').DataTable({
            "paging": true,
            "lengthChange": true,
            "searching": true,
            "ordering": true,
            "info": true,
            "autoWidth": false,
            "responsive": true,
            "bDestroy": true,
            "data": data,
            "columns": [
                { "data": "flight_num"},
                { "data": "origin" },
                { "data": "origin_city" },
                { "data": "origin_country" },
                { "data": "dest" },
                { "data": "dest_city" },
                { "data": "dest_country" }
            ],
           "createRow": function (row, data, dataIndex) {
                if (data.intl === true) {
                    $(row).addClass('red');
                }
           }
        });
    });
}