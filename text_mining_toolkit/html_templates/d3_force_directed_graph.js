console.log(d3);

var width = 640,
    height = 480;

var svg = d3.select("#d3-container")
    .append("svg")
    .attr("width", width)
    .attr("height", height);

var simulation = d3.forceSimulation();
