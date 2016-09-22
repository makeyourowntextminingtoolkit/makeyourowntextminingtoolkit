// require is needed to make d3 work in a noebooks from imported code
require.config({
    paths: {
        d3: "https://d3js.org/d3.v4.min"
    }
});

require(["d3"], function(d3) {
    //console.log(d3.version);

    var width = 640,
        height = 480;

    var svg = d3.select("#d3-container-%%unique-id%%")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

    var colour = d3.scaleOrdinal(d3.schemeCategory20);

    var graph = {
        nodes: %%nodes%%,
        links: %%links%%
    };

    var simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink(graph.links))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2.0, height / 2.0));

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
        .attr("r", 4.5)
        .style("fill", function (d) {return colour(d.weight);})
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("title")
        .text(function(d) { return d.id; });

    /* node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(function(d) { return d.id }); */

    simulation
        .on("tick", ticked);

    function ticked() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    };

    function dragstarted(d) {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    };

    function dragged(d) {
        d.fx = d3.event.x;
        d.fy = d3.event.y;
    };

    function dragended(d) {
        if (!d3.event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    };

});

