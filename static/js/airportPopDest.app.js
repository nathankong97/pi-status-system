var params = new URLSearchParams(window.location.search);
var airport = String(params.get('airport-input'));
var url = '/api/v1/airport/pop_destination/' + airport;

fetch(url)
  .then((response) => {
    return response.json();
  })
  .then((myJson) => {
      generateDestTable(myJson.data);
  });

function generateDestTable(data) {
    var content = "";
    var i;
    for (i = 0; i < data.length; i++) {
      var item = data[i];
      content += "<tr><td>" + item.name + "</td>";
      content += "<td>" + item.city + "</td>";
      content += "<td>" + item.count + "</td>";
      content += "<td>" + item.carrier + "</td></tr>";
    }
    document.getElementById("pop-destination-table").innerHTML = content;
}