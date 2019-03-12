var width = 800;
var height = 800;

d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g");

var svg = d3.select("svg");

d3.json("../data/master_5000.json").then(function(data) {
    console.log(data);

    var xScale = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return timeToSeconds(d.length); })])
		//.range([padding, w - padding * 2]);

	var yScale = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return d.purchase_date; })])
		//.range([h - padding, padding]);
});

function timeToSeconds(time) {
    elements = time.split(":");
    hoursToSeconds = elements[0] * 3600;
    minutesToSeconds = elements[1] * 60;
    return hoursToSeconds + minutesToSeconds + elements[2];
}
