var width = 800;
var height = 800;
var padding = 100;

d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g");

var svg = d3.select("svg");

d3.json("../data/master_5000.json").then(function(data) {
    data = data.filter(function(d) { return d.purchase_date != null})

    data.forEach(function(d) {
        d.purchase_date = new Date(d.purchase_date);
    });

    var xScale = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return timeToSeconds(d.length); })])
		.range([padding, width - padding * 2]);

	var yScale = d3.scaleLinear()
		.domain(d3.extent(data, getPurchaseDate))
		.range([height - padding, padding]);

    svg.selectAll("circle")
			.data(data)
			.enter()
			.append("circle")
			.attr("cx", function(d) {
				return xScale(timeToSeconds(d.length));
			})
			.attr("cy", function(d) {
			    return height - yScale(d.purchase_date);
			})
			.attr("r", 5)
			.attr("fill", "green");

	svg.append("g")
	    .attr("transform", "translate(0," + (height - padding) + ")")
        .call(d3.axisBottom(xScale));

    svg.append("g")
    	.attr("transform", "translate(" + padding + ", 0)")
        .call(d3.axisLeft(yScale));

});

function getPurchaseDate(d) {
    return d.purchase_date;
}

function timeToSeconds(time) {
    console.log(time)
    elements = time.split(":");
    hoursToSeconds = Number(elements[0]) * 3600;
    minutesToSeconds = Number(elements[1]) * 60;
    return hoursToSeconds + minutesToSeconds + Number(elements[2]);
}
