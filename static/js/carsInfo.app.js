var params = new URLSearchParams(window.location.search);
var model = String(params.get('model'));
var zipcode = String(params.get('zipcode'));


console.log(model);
console.log(zipcode);

var url = "/api/v1/carsInfo/" + model + "/" + zipcode;

fetch(url)
    .then((response) => {
        return response.json();
    })
    .then((myJson) => {
        var table = new Tabulator("#carInfoTable", {
            pagination:"local",
            paginationSize:20,
            paginationInitialPage:2,
            paginationSizeSelector:[5, 10, 15, 20, 30, 50],
            movableColumns:false,
            data: myJson, //assign data to table
            layout: "fitColumns", //fit columns to width of table (optional)
            columns: [ //Define Table Columns
                {title: "ID", field: "id", width: 150},
                {title: "Model", field: "model"},
                {title: "Trim", field: "trim"},
                {title: "Year", field: "year"},
                {title: "Style", field: "style"},
                {title: "Stock Type", field: "stockType"},
                {title: "Driver Wheel", field: "driver_wheel"},
                {title: "Fuel Type", field: "fuel_type"},
                {title: "Color", field: "color"},
                {title: "Interior Color", field: "interior_color"},
                {title: "Mileage", field: "mileage"},
                {title: "Price", field: "price"}
            ]
        });
    });
