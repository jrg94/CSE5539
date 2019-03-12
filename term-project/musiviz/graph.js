var width = 800;
var height = 800;

d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g");

var svg = d3.select("svg");

d3.json("../data/master_5000.json").then(function(data) {
    console.log(data);
});
