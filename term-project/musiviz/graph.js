var width = 800;
var height = 800;
var padding = 50;

d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height);

var svg = d3.select("svg");

/**
 * Generates the release date vs. duration graph on the current SVG.
 *
 * @param {Object} data - a music object
 */
function durationVsReleaseDate(data) {
    // Filter out useless data
    data = data.filter(filterReleaseDate)

    // Update purchase date from string to date object
    data.forEach(function(d) {
        d.release_date = new Date(d.release_date);
    });

    // Create x scale
    var yScale = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return timeToSeconds(d.length); })])
	    .range([height - padding, padding]);

    // Create y scale
	var xScale = d3.scaleTime()
		.domain(d3.extent(data, function(d) { return d.release_date; }))
		.range([padding, width - padding * 2]);

    // Create color scale
	var colorScale = d3.scaleOrdinal(d3.schemePaired);

    // Draw all circles
    svg.selectAll("circle")
		.data(data)
		.enter()
		.append("circle")
		.attr("cy", function(d) {
			return yScale(timeToSeconds(d.length));
		})
		.attr("cx", function(d) {
		    return xScale(d.release_date);
		})
		.attr("r", 5)
		.attr("fill", function(d) { return colorScale(d.genre); } );

    // Draw x-axis
	svg.append("g")
	    .attr("transform", "translate(0," + (height - padding) + ")")
        .call(d3.axisBottom(xScale));

    // Draw x-axis title
    svg.append("text")
        .attr("transform", "translate(" + ((width/2) - padding / 2) + " ," + (height - 10) + ")")
        .style("text-anchor", "middle")
        .text("Purchase Date (Year)");

    // Draw y-axis
    svg.append("g")
    	.attr("transform", "translate(" + padding + ", 0)")
        .call(d3.axisLeft(yScale));

    // Draw y-axis title
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 5)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Time (seconds)");

    // Create legend
    var legend = svg.selectAll(".legend")
        .data(colorScale.domain())
        .enter().append("g")
        .attr("class","legend")
        .attr("transform", function(d,i) {
            return "translate(0," + i * 20 + ")";
        });

    // Draw color rectangles on legend
    legend.append("rect")
        .attr("x",width - padding)
        .attr("y",9)
        .attr("width",18)
        .attr("height",18)
        .style("fill", colorScale);

    // Draw legend text
    legend.append("text")
        .attr("x",width - padding - 10)
        .attr("y",18)
        .attr("dy",".35em")
        .style("text-anchor","end")
        .text(function(d) {
            return d;
        });

    // Draw title
    svg.append("text")
	   .attr("class", "title")
	   .attr("dy", padding / 2)
	   .attr("dx", ((width/2) - padding / 2))
	   .style("text-anchor", "middle")
	   .style("font-size", "20px")
       .style("text-decoration", "underline")
	   .text("Duration vs. Purchase Date")
}

/**
 * Generates the release date vs. duration graph on the current SVG.
 *
 * @param {Object} data - a music object
 */
function durationVsPurchaseDate(data) {
    // Filter out useless data
    data = data.filter(filterPurchaseDate)

    // Update purchase date from string to date object
    data.forEach(function(d) {
        d.purchase_date = new Date(d.purchase_date);
    });

    // Create x scale
    var yScale = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return timeToSeconds(d.length); })])
	    .range([height - padding, padding]);

    // Create y scale
	var xScale = d3.scaleTime()
		.domain(d3.extent(data, getPurchaseDate))
		.range([padding, width - padding * 2]);

    // Create color scale
	var colorScale = d3.scaleOrdinal(d3.schemePaired);

    // Draw all circles
    svg.selectAll("circle")
		.data(data)
		.enter()
		.append("circle")
		.attr("cy", function(d) {
			return yScale(timeToSeconds(d.length));
		})
		.attr("cx", function(d) {
		    return xScale(d.purchase_date);
		})
		.attr("r", 5)
		.attr("fill", function(d) { return colorScale(d.genre); } );

    // Draw x-axis
	svg.append("g")
	    .attr("transform", "translate(0," + (height - padding) + ")")
        .call(d3.axisBottom(xScale));

    // Draw x-axis title
    svg.append("text")
        .attr("transform", "translate(" + ((width/2) - padding / 2) + " ," + (height - 10) + ")")
        .style("text-anchor", "middle")
        .text("Purchase Date (Year)");

    // Draw y-axis
    svg.append("g")
    	.attr("transform", "translate(" + padding + ", 0)")
        .call(d3.axisLeft(yScale));

    // Draw y-axis title
    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - 5)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("Time (seconds)");

    // Create legend
    var legend = svg.selectAll(".legend")
        .data(colorScale.domain())
        .enter().append("g")
        .attr("class","legend")
        .attr("transform", function(d,i) {
            return "translate(0," + i * 20 + ")";
        });

    // Draw color rectangles on legend
    legend.append("rect")
        .attr("x",width - padding)
        .attr("y",9)
        .attr("width",18)
        .attr("height",18)
        .style("fill", colorScale);

    // Draw legend text
    legend.append("text")
        .attr("x",width - padding - 10)
        .attr("y",18)
        .attr("dy",".35em")
        .style("text-anchor","end")
        .text(function(d) {
            return d;
        });

    // Draw title
    svg.append("text")
	   .attr("class", "title")
	   .attr("dy", padding / 2)
	   .attr("dx", ((width/2) - padding / 2))
	   .style("text-anchor", "middle")
	   .style("font-size", "20px")
       .style("text-decoration", "underline")
	   .text("Duration vs. Purchase Date")
}

/**
 * Filters the data set to exclude:
 *   - null release dates
 *   - null genres
 *   - Comedy songs
 *   - Country songs
 *   - Soundtrack songs
 *
 * @param {Object} data - a music object
 * @returns {boolean} true if none of the items listed above
 */
function filterReleaseDate(data) {
    var p = data.release_date != null;
    var g = data.genre != null;
    var c = data.genre != "Comedy";
    var u = data.genre != "Country";
    var s = data.genre != "Soundtrack";
    return p && g && c && u && s;
}

/**
 * Filters the data set to exclude:
 *   - null purchase dates
 *   - null genres
 *   - Comedy songs
 *   - Country songs
 *   - Soundtrack songs
 *
 * @param {Object} data - a music object
 * @returns {boolean} true if none of the items listed above
 */
function filterPurchaseDate(data) {
    var p = data.purchase_date != null;
    var g = data.genre != null;
    var c = data.genre != "Comedy";
    var u = data.genre != "Country";
    var s = data.genre != "Soundtrack";
    return p && g && c && u && s;
}

/**
 * Retrieves the purchase date from the music object.
 *
 * @param {Object} data - a music object
 * @returns {Date} a purchase date
 */
function getPurchaseDate(data) {
    return data.purchase_date;
}

/**
 * Converts a time string to seconds.
 *
 * @param {string} - time a time string in the format HH:MM:SS
 * @returns {number} the time string as a number in seconds
 */
function timeToSeconds(time) {
    elements = time.split(":");
    hoursToSeconds = Number(elements[0]) * 3600;
    minutesToSeconds = Number(elements[1]) * 60;
    return hoursToSeconds + minutesToSeconds + Number(elements[2]);
}
