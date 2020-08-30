Plotly.d3.csv('fox-wolf.csv', function(err, rows){

  function unpack(rows, key) {
  return rows.map(function(row) { return row[key]; });
  }

  var headerNames = Plotly.d3.keys(rows[0]);

  var headerValues = [];
  var cellValues = [];
  for (i = 0; i < headerNames.length; i++) {
    headerValue = [headerNames[i]];
    headerValues[i] = headerValue;
    cellValue = unpack(rows, headerNames[i]);
    cellValues[i] = cellValue;
  }

  // clean date
  for (i = 0; i < cellValues[1].length; i++) {
  var dateValue = cellValues[1][i].split(' ')[0]
  cellValues[1][i] = dateValue
  }

var Blue='#1f77b4';
var LightBlue='#A6E7E4';   
var color1='rgb(235, 193, 238)';
var color2='rgba(228, 222, 249, 0.65)';
var data = [{
  type: 'table',
//  columnwidth: [150,600,1000,900,600,500,1000,1000,1000],
//  columnorder: [0,1,2,3,4,5,6,7,8,9],
  header: {
    values: headerValues,
    align: "center",
    line: {width: 1, color: 'rgb(50, 50, 50)'},
    fill: {color: [Blue]},
    font: {family: "Arial", size: 10, color: "white"}
  },
  cells: {
    values: cellValues,
    align: ["center", "center"],
    line: {color: "black", width: 1},
    fill: {color: [Blue,LightBlue,LightBlue,LightBlue,LightBlue,Blue,LightBlue,LightBlue,LightBlue,LightBlue,LightBlue,Blue]},
    font: {family: "Arial", size: 9, color: ["black"]}
  }
}]

var layout = {
  title: "FOX-WOLF BASIN HYDROLOGIC DATA HOURLY LEVELS AND FLOWS",
   autosize: true,
  // rangemode: "tozero",
  //width: 500,
  height: 1000,
}

Plotly.newPlot('table1', data, layout);
});
