const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

const show_tooltip = function (text) {
    tooltip.transition()
        .duration(100)
        .style("opacity", .9);
    tooltip.html(text ? text : "Hmm... I wonder what this means?")
        .style("left", (d3.event.pageX) + "px")
        .style("top", (d3.event.pageY) + "px");
}

const hide_tooltip = function () {
    tooltip.transition()
        .duration(200)
        .style("opacity", 0);
}


const sidebar = d3.select("body").append("div")
    .attr("class", "sidebar");

const show_sidebar = function (d_this) {
    sidebar.transition()
        .duration(100)
        .style("left", "0");
    sidebar.html("<h2>" + d_this.label + "</h2><div>"
        + (d_this.description ? d_this.description : "Hmm... I wonder what this means?")
        + "</div>");
}

const hide_sidebar = function () {
    sidebar.transition()
        .duration(600)
        .style("left", "-300px");
}
