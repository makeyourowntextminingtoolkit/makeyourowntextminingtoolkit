// require is need to make d3 work in a noebooks from imported code
require.config({
    paths: {
        d3: "https://d3js.org/d3.v4.min"
    }
});

require(["d3"], function(d3) {
    // run
    d3.select("#d3-container-%%unique-id%%").append("h1").text("Successfully loaded D3 version " + d3.version);
    console.log(d3.version);

    var width = 640,
        height = 480;

    var svg = d3.select("#d3-container-%%unique-id%%")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    console.log("test2");


    var graph = {
        "nodes": [
            {"id": "apple"},
            {"id": "banana"},
            {"id": "cherry"}
        ],
        "links": [
            {"source": 0, "target": 1},
            {"source": 1, "target": 2}
        ]
    };

    var link = svg.append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(graph.links)
        .enter().append("line");

    var node = svg.append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("r", 2.5);

    var simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink())
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width/2, height/2));

    /* var simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink().id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2)); */

    simulation
        .on("tick", ticked);

    simulation.force("link")
        .links(graph.links);

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    }

});

