
var url = "/api/v1/flightDateCount"

$("#loadingMessage").html('<img src="{{url_for(\'static\', filename=\'./images/loading.gif\')}}" alt="" srcset="">');
fetch(url)
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        $("#loadingMessage").html("");
        var ctx = document.getElementById("myChart");
        var myChart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels: data.label,
            datasets: [
              {
                label: 'Count',
                data: data.count
              }
            ]
          }
        });
    })