var width = 800;
var height = 800;
var padding = 50;

d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height)
  .append("g");

var svg = d3.select("svg");

d3.json("../data/master_5000.json").then(lengthVsDate);

function lengthVsDate(data) {
    data = data.filter(filter)

    data.forEach(function(d) {
        d.purchase_date = new Date(d.purchase_date);
    });

    var xScale = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return timeToSeconds(d.length); })])
		.range([padding, width - padding * 2]);

	var yScale = d3.scaleTime()
		.domain(d3.extent(data, getPurchaseDate))
		.range([height - padding, padding]);

	var colorScale = d3.scaleOrdinal(d3.schemeSet3);

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
			.attr("fill", function(d) { return colorScale(d.genre); } );

	svg.append("g")
	    .attr("transform", "translate(0," + (height - padding) + ")")
        .call(d3.axisBottom(xScale));

    svg.append("g")
    	.attr("transform", "translate(" + padding + ", 0)")
        .call(d3.axisLeft(yScale));

    var legend = svg.selectAll(".legend")
        .data(colorScale.domain())
        .enter().append("g")
        .attr("class","legend")
        .attr("transform",function(d,i) {
            return "translate(0," + i * 20 + ")";
        });

    legend.append("rect")
        .attr("x",width - padding)
        .attr("y",9)
        .attr("width",18)
        .attr("height",18)
        .style("fill", colorScale);

    legend.append("text")
        .attr("x",width - padding - 10)
        .attr("y",18)
        .attr("dy",".35em")
        .style("text-anchor","end")
        .text(function(d) {
            return d;
        });

}

function filter(data) {
    var p = data.purchase_date != null;
    var g = data.genre != null;
    var c = data.genre != "Comedy";
    var u = data.genre != "Country";
    var s = data.genre != "Soundtrack";
    return p && g && c && u && s;
}

function getPurchaseDate(d) {
    return d.purchase_date;
}

function timeToSeconds(time) {
    elements = time.split(":");
    hoursToSeconds = Number(elements[0]) * 3600;
    minutesToSeconds = Number(elements[1]) * 60;
    return hoursToSeconds + minutesToSeconds + Number(elements[2]);
}
