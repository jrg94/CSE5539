var width = 800;
var height = 800;
var padding = 50;

d3.select("body").append("svg")
  .attr("width", width)
  .attr("height", height);

var svg = d3.select("svg");

function genreHistogram(data) {

  var mapping = []
  data.forEach(function(d) {
    if (d.genre == null) {
      d.genre = "None";
    }
    var found = false;
    for (var i = 0; i < mapping.length && !found; i++) {
      if (mapping[i].genre == d.genre) {
        mapping[i].count += 1;
        found = true;
      }
    }
    if (!found) {
      mapping.push({
        "genre": d.genre,
        "count": 1
      })
    }
  });
  mapping.sort((a, b) => b.count - a.count)

  var xScale = d3.scaleBand()
    .domain(mapping.map(function(d) {
      return d.genre;
    }))
    .range([padding, width - padding * 2])
    .padding(.1);

  var yScale = d3.scaleLinear()
    .domain([0, d3.max(mapping, function(d) {
      return d.count;
    })])
    .range([height - padding, padding]);

  svg.append("g")
    .attr("transform", "translate(0," + (height - padding) + ")")
    .call(d3.axisBottom(xScale))
    .selectAll("text")
    .style("text-anchor", "end")
    .attr("dx", "-.8em")
    .attr("dy", ".15em")
    .attr("transform", "rotate(-35)");

  // Draw y-axis
  svg.append("g")
    .attr("transform", "translate(" + padding + ", 0)")
    .call(d3.axisLeft(yScale));

  svg.selectAll(".bar")
    .data(mapping)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("fill", "#dc3912")
    .attr("x", function(d) {
      return xScale(d.genre);
    })
    .attr("y", function(d) {
      return yScale(d.count);
    })
    .attr("width", xScale.bandwidth())
    .attr("height", function(d) {
      return height - yScale(d.count) - padding;
    });

  drawTitle("Genre Histogram");
}

/**
 * Plots dBFS over Release Date.
 */
function dBFSVsReleaseDate(data) {
  // Filter out useless data
  data = data.filter(filterReleaseDate)

  // Update purchase date from string to date object
  data.forEach(function(d) {
    d.release_date = new Date(d.release_date);
  });

  // Create x scale
  var yScale = d3.scaleLinear()
    .domain([d3.min(data, d => d.dBFS), 0])
    .range([height - padding, padding]);

  // Create y scale
  var xScale = d3.scaleTime()
    .domain(d3.extent(data, function(d) {
      return d.release_date;
    }))
    .range([padding, width - padding * 2]);

  // Create color scale
  var colorScale = d3.scaleOrdinal(d3.schemePaired);

  drawCircles(data, d => yScale(d.dBFS), d => xScale(d.release_date), d => colorScale(d.genre));
  drawXAxis(xScale, padding, height, width, "Release Date (Year)");
  drawYAxis(yScale, padding, height, "dBFS");
  drawLegend(colorScale);
  drawTitle("dBFS vs. Release Date");
}

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
    .domain([0, d3.max(data, function(d) {
      return timeToSeconds(d.length);
    })])
    .range([height - padding, padding]);

  // Create y scale
  var xScale = d3.scaleTime()
    .domain(d3.extent(data, function(d) {
      return d.release_date;
    }))
    .range([padding, width - padding * 2]);

  // Create color scale
  var colorScale = d3.scaleOrdinal(d3.schemePaired);

  drawCircles(data, d => yScale(timeToSeconds(d.length)), d => xScale(d.release_date), d => colorScale(d.genre));
  drawXAxis(xScale, padding, height, width, "Release Date (Year)")
  drawYAxis(yScale, padding, height, "Duration (seconds)");
  drawLegend(colorScale);
  drawTitle("Duration vs. Release Date");
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
    .domain([0, d3.max(data, function(d) {
      return timeToSeconds(d.length);
    })])
    .range([height - padding, padding]);

  // Create y scale
  var xScale = d3.scaleTime()
    .domain(d3.extent(data, getPurchaseDate))
    .range([padding, width - padding * 2]);

  // Create color scale
  var colorScale = d3.scaleOrdinal(d3.schemePaired);

  drawCircles(data, d => yScale(timeToSeconds(d.length)), d => xScale(d.purchase_date), d => colorScale(d.genre));
  drawXAxis(xScale, padding, height, width, "Purchase Date (Year)")
  drawYAxis(yScale, padding, height, "Duration (seconds)");
  drawLegend(colorScale);
  drawTitle("Duration vs. Purchase Date");
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
  var c = data.genre != "Vocal";
  var u = data.genre != "Dance";
  var s = data.genre != "Instrumental";
  var r = data.genre != "Hip-Hop";
  return p && g && c && u && s && r;
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

/**
 * Draws circles.
 *
 * @param data - the data for circle drawing
 * @param cx - a function for the x position
 * @param cy - a function for the y position
 * @param fill - a function for the color
 */
function drawCircles(data, cx, cy, fill) {
  svg.selectAll("circle")
    .data(data)
    .enter()
    .append("circle")
    .attr("cy", cx)
    .attr("cx", cy)
    .attr("r", 5)
    .attr("fill", fill);
}

/**
 * Draws the x-axis.
 *
 * @param xScale - a D3 scale object
 * @param padding - the padding
 * @param height - the height of the SVG
 * @param width - the width of the SVG
 * @param label - the x-axis label
 */
function drawXAxis(xScale, padding, height, width, label) {
  // Draw x-axis
  svg.append("g")
    .attr("transform", "translate(0," + (height - padding) + ")")
    .call(d3.axisBottom(xScale));

  // Draw x-axis title
  svg.append("text")
    .attr("transform", "translate(" + ((width / 2) - padding / 2) + " ," + (height - 10) + ")")
    .style("text-anchor", "middle")
    .text(label);
}

/**
 * Draws the y-axis.
 *
 * @param yScale - a D3 scale object
 * @param padding - the padding
 * @param height - the height of the SVG
 * @param label - the y-axis label
 */
function drawYAxis(yScale, padding, height, label) {
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
    .text(label);
}

/**
 * Draws a title on the master SVG
 *
 * @param {string} title - the title to be drawn
 */
function drawTitle(title) {
  svg.append("text")
    .attr("class", "title")
    .attr("dy", padding / 2)
    .attr("dx", ((width / 2) - padding / 2))
    .style("text-anchor", "middle")
    .style("font-size", "20px")
    .style("text-decoration", "underline")
    .text(title)
}

/**
 * Draws a legend on the master svg
 *
 * @param {Object} colorScale - a color scale
 */
function drawLegend(colorScale) {
  // Create legend
  var legend = svg.selectAll(".legend")
    .data(colorScale.domain())
    .enter().append("g")
    .attr("class", "legend")
    .attr("transform", function(d, i) {
      return "translate(0," + i * 20 + ")";
    });

  // Draw color rectangles on legend
  legend.append("rect")
    .attr("x", width - padding)
    .attr("y", 9)
    .attr("width", 18)
    .attr("height", 18)
    .style("fill", colorScale);

  // Draw legend text
  legend.append("text")
    .attr("x", width - padding - 10)
    .attr("y", 18)
    .attr("dy", ".35em")
    .style("text-anchor", "end")
    .text(function(d) {
      return d;
    });
}
