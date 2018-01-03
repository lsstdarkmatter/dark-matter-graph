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


var sidebar_has_instruction;
const sidebar = d3.select("body").append("div")
  .attr("class", "sidebar");


const prepare_sidebar_content = function (d_this) {
  sidebar.append("h2").text(d_this.label);
  sidebar.append("div").text(d_this.description ? d_this.description : "Hmm... I wonder what this means?");
  if (d_this.references) {
    sidebar.append("h3").text("References");
    let ul = sidebar.append("ul");
    ul.selectAll("li")
      .data(d_this.references)
      .enter().append("li")
      .html(r => "<a href='https://ui.adsabs.harvard.edu/#abs/" + r.ads + "/abstract'>" + r.text + "</a>");
  }
};

const show_sidebar = function (d_this, raw_html = false, append = false) {
  sidebar.transition()
    .duration(200)
    .style("left", "0");
  if (sidebar_has_instruction || !append) sidebar.html("");
  if (raw_html) sidebar.html(sidebar.html() + d_this);
  else prepare_sidebar_content(d_this);
  sidebar.selectAll("*").on("click", () => { d3.event.stopPropagation(); });
  sidebar_has_instruction = false;
}

const hide_sidebar = function () {
  sidebar.transition()
    .duration(600)
    .style("left", "-300px");
}

const load_instruction = function (name) {
  d3.text("static/instruction_" + name + ".html", function (error, ht) {
    if (error) throw error;
    show_sidebar(ht, true);
    sidebar_has_instruction = true;
  });
};

sidebar.on("click", hide_sidebar);
