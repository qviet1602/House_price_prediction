var states_div_width = 250;
var states_div_height = 600;
var dynamic_trends_div_width = 700;
var chart_height = 300;
var states_bar_height = 50;
var parseTime = d3.timeParse("%Y");
var left_margin = 60;
var bottom_margin = 60;
var promises = [
  d3.json('/api/list_counties_rental/'),
  d3.json('/api/county_data_rental/'),
];

Promise.all(promises).then(ready);
var global_state_data = []
function load_loading_bar() {
    d3.select("#loading_svg").remove();
    var loading_svg = d3.select("#chart1_dummy_svg").append("svg");
    loading_svg.attr("width", dynamic_trends_div_width)
                .attr("id", "loading_svg")
                .attr("height", 50);

    loading_svg
      .append("text")
      .attr("x", dynamic_trends_div_width / 2)
      .attr("y", 25)
      .attr("text-anchor", "middle")
      .attr("font-size", "16px")
      .attr("font-family", "Helvetica")
      .style("fill", "red")
      .style("stroke-width", 3)
      .text("Loading... Please wait");

    loading_svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", dynamic_trends_div_width)
                .attr("height", 100)
                .style("stroke", "black")
                .style("fill", "green")
                .style("opacity", "0.2")
                .style("stroke-width", 1);
}
load_loading_bar();
function ready([state_list, state_data]) {
    d3.select("#loading_svg").remove();
	global_state_data = state_list;
	var num_states = state_list.length;
	var total_svg_height = states_bar_height * num_states;
	var states_list_svg = d3.select(".states_div").append("svg");
	states_list_svg.attr("width", states_div_width)
		       .attr("height", total_svg_height)

	var bar = states_list_svg.selectAll("g")
    			     .data(state_list)
  			     .enter().append("g")
    			     .attr("transform", function(d, i) {
				return "translate(0," + i * states_bar_height + ")";
			     });

	bar.append("rect")
    	   .attr("width", states_div_width)
    	   .attr("height", states_bar_height - 1)
 	   .style("fill", "steelblue")
	   .on("click", handleStateClick);

	bar.append("text")
    	   .attr("x", 10)
    	   .attr("y", states_bar_height / 2)
     	   .attr("dy", ".35em")
           .attr("font-family", "Arial")
           .style("fill", "white")
    	   .text(function(d) { return d['name']; })
    	   .on("click", handleStateClick);

	//Draw line chart here given this data
        draw_lineChart1(state_data);
        draw_barChart1(state_data[0]['singleFamilyResidenceRental']);
        draw_barChart2(state_data[1]['multiFamilyResidenceRental']);
	all_rectangles = d3.selectAll("rect");
        all_rectangles.each(function(d, i) {
		if(d['name'] != null && d['id'] != null && d['id'] == 706) {
                	d3.select(this).style("fill", "green");
		}
        })
}

function handleStateClick(d_out) {
	all_rectangles = d3.selectAll("rect");
	all_rectangles.each(function(d, i) {
	    if(d['name'] != null) {
	        if(d_out['name'] != null && d['name'] != null && d_out['name'] == d['name']) {
	            d3.select(this).style("fill", "green")
	        } else {
	            d3.select(this).style("fill", "steelblue");
	        }
	    }
	})
	clicked_state_id = d_out['id']
	d3.select("#line_chart1").remove();
	d3.select("#line_chart2").remove();
	d3.select("#line_chart3").remove();
    load_loading_bar()
	var state_promise = [
  		d3.json('/api/county_data_rental/?county_id=' + clicked_state_id),
	];

	Promise.all(state_promise).then(state_data_ready);
}

function state_data_ready([state_data]) {
    d3.select("#loading_svg").remove();
	//Draw line chart here given this data
	draw_lineChart1(state_data);
	draw_barChart1(state_data[0]['singleFamilyResidenceRental'])
	draw_barChart2(state_data[1]['multiFamilyResidenceRental'])
}

function draw_lineChart1(state_data) {
    d3.select("#line_chart1").remove();
	singleFamilyResidenceRental_data = state_data[0]['singleFamilyResidenceRental']
	multiFamilyResidenceRental_data = state_data[1]['multiFamilyResidenceRental']

	min_multiFamilyResidenceRental_year = d3.min(multiFamilyResidenceRental_data, function(d) {
                return parseTime(d.year);
        });

    min_singleFamilyResidenceRental_year = d3.min(singleFamilyResidenceRental_data, function(d) {
                return parseTime(d.year);
        });


    min_multiFamilyResidenceRental_price = d3.min(multiFamilyResidenceRental_data, function(d) {
                return parseInt(d.list_price);
        });

    min_singleFamilyResidenceRental_price = d3.min(singleFamilyResidenceRental_data, function(d) {
                return parseInt(d.list_price);
        });

	chart1_all_min_years = []

	chart1_all_min_years.push(min_multiFamilyResidenceRental_year);
	chart1_all_min_years.push(min_singleFamilyResidenceRental_year);

	min_year = d3.min(chart1_all_min_years);

	chart1_all_min_prices = []

	chart1_all_min_prices.push(min_multiFamilyResidenceRental_price);
	chart1_all_min_prices.push(min_singleFamilyResidenceRental_price);

	min_price = d3.min(chart1_all_min_prices);

	max_multiFamilyResidenceRental_year = d3.max(multiFamilyResidenceRental_data, function(d) {
                return parseTime(d.year);
        });

        max_singleFamilyResidenceRental_year = d3.max(singleFamilyResidenceRental_data, function(d) {
                return parseTime(d.year);
        });

	max_multiFamilyResidenceRental_price = d3.max(multiFamilyResidenceRental_data, function(d) {
                return parseInt(d.list_price);
        });

        max_singleFamilyResidenceRental_price = d3.max(singleFamilyResidenceRental_data, function(d) {
                return parseInt(d.list_price);
        });

	chart1_all_max_years = []

        chart1_all_max_years.push(max_multiFamilyResidenceRental_year);
        chart1_all_max_years.push(max_singleFamilyResidenceRental_year);

        max_year = d3.max(chart1_all_max_years);


        chart1_all_max_prices = []

        chart1_all_max_prices.push(max_multiFamilyResidenceRental_price);
        chart1_all_max_prices.push(max_singleFamilyResidenceRental_price);


        max_price = d3.max(chart1_all_max_prices);

	var chart1_svg = d3.select("#chart1_dummy_svg").append("svg");
	chart1_svg.attr("width", dynamic_trends_div_width)
		  .attr("id", "line_chart1")
		  .attr("height", chart_height);

	var tick_values_x = []
        tick_values_x.push(min_year);
        var current_year = min_year;
        while (current_year.getFullYear() < max_year.getFullYear()) {
                var next_year = current_year.getFullYear() + 5;
                var next_date = parseTime(next_year);
                tick_values_x.push(next_date);
                current_year = next_date;
        }

        var x_axisScale = d3.scaleTime().domain([ min_year, max_year ])
					.nice()
					.range(
                        [ left_margin, dynamic_trends_div_width - left_margin ]);

        var xAxis = d3.axisBottom(x_axisScale)
		      .ticks(d3.timeYear.every(2));

        // Translate the xAxis
        new_xAxis_x_pos = 0;
        new_xAxis_y_pos = chart_height - bottom_margin;
        var translate_xAxis_by = "translate(" + new_xAxis_x_pos + ","
                        + new_xAxis_y_pos + ")";
        chart1_svg.append("g").attr("class", "axis").attr("transform",
                        translate_xAxis_by).call(xAxis);

	// Draw y axis

	var y_axisScale = d3.scaleLinear().domain(
                        [ 0, max_price ]).range(
                        [ chart_height - bottom_margin, left_margin ]);

        new_yAxis_x_pos = left_margin;
        new_yAxis_y_pos = 0;
        var translate_yAxis_by = "translate(" + new_yAxis_x_pos + ","
                        + new_yAxis_y_pos + ")";

        var yAxis = d3.axisLeft().scale(y_axisScale);

        chart1_svg.append("g").attr("class", "axis").attr("transform",
                        translate_yAxis_by).call(yAxis);

	chart1_svg.append("text").attr("class", "x label").attr("x", dynamic_trends_div_width / 2).attr("y",
                        chart_height - 20).attr("text-anchor", "middle").attr(
                        "font-size", "16px").attr(
                                        "font-family", "Helvetica").text("Year");
    //Set a label for the y-axis
        chart1_svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -5)
    .attr("x",0 - (chart_height / 2))
    .attr("dy", "1em")
    .attr("font-family", "Helvetica")
    .style("text-anchor", "middle")
    .text("Price");
	//Draw lines
	var all_colors = d3.schemeCategory10;
        var colorScheme = {'multiFamilyResidenceRental': '#FFC300', 'singleFamilyResidenceRental': '#FF5733'}



        var line = d3.line()
                                  .x(function(d) {
                                          return x_axisScale(parseTime(d.year));
                                  })
                                  .y(function(d) {
                                          return y_axisScale(parseInt(d.list_price));
                                  })
                                  .curve(d3.curveMonotoneX)
                                  ;
	chart1_svg.append("path")
                          .datum(multiFamilyResidenceRental_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['multiFamilyResidenceRental']);

         chart1_svg.append("path")
                          .datum(singleFamilyResidenceRental_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['singleFamilyResidenceRental']);


	//Draw the legend
        var legend_names = ['multiFamilyResidenceRental', 'singleFamilyResidenceRental']
        chart1_svg.selectAll("legend_rect")
                          .data(legend_names)
                          .enter()
                          .append("rect")
                          .attr("x", 400)
                          .attr("y", function(d, i) {
                                  return 10 + (i * 20);
                          })
                          .attr("width", 30)
                          .attr("height", 10)
                          .style("fill", function(d) {
                                  return colorScheme[d];
                          });

         chart1_svg.selectAll("legend_label")
          .data(legend_names)
          .enter()
          .append("text")
          .attr("x", 440)
          .attr("y", function(d, i) {
                  return 20 + (i * 20);
          })
          .attr("width", 30)
          .attr("height", 10)
          .attr("text-anchor", "left")
          .attr("font-family", "Helvetica")
          .text(function(d){ return d})
          .style("fill", function(d) {
                  return colorScheme[d];
          })
          .style("alignment-baseline", "middle");
}

function draw_barChart1(feature_data) {
    d3.select("#line_chart2").remove();
    var chart2_svg = d3.select("#chart2_dummy_svg").append("svg");
	chart2_svg.attr("width", dynamic_trends_div_width)
		  .attr("id", "line_chart2")
		  .attr("height", 500);

    var margin = {}
    margin['left_margin'] = 10
    margin['right_margin'] = 10
    margin['top_margin'] = 100
    margin['bottom_margin'] = 100

    chart2_svg.append("text")
                      .attr("x", dynamic_trends_div_width/2)
                      .attr("y", margin['top_margin']/2)
                      .attr("text-anchor", "middle")
                      .attr("font-size", "16px")
                      .text("Bar chart (singleFamilyResidenceRental)")


	min_year = d3.min(feature_data, function(d) {
                return parseTime(d.year);
        });
    max_year = d3.max(feature_data, function(d) {
                return parseTime(d.year);
        });

    min_price = d3.min(feature_data, function(d) {
                return parseInt(d.list_price);
        });
    max_price = d3.max(feature_data, function(d) {
                return parseInt(d.list_price);
        });


     var y_axisScale = d3.scaleLinear()
                                  .domain([0, max_price])
                                  .range([500 - margin['bottom_margin'], margin['top_margin']]);

                   var yAxis = d3.axisLeft()
                                 .scale(y_axisScale);

                   y_val = 500 - margin['bottom_margin']

                   var translate_yAxis_by = "translate(40,0)";
                   chart2_svg.append("g")
                      .attr("class", "axis")
                      .attr("transform", translate_yAxis_by)
                      .call(yAxis);



    //Draw x axis

    var x_axisScale = d3.scaleTime()
                                  .domain([min_year, max_year])
                                  .range([40, dynamic_trends_div_width - 100]);

    var xAxis = d3.axisBottom(x_axisScale);

        // Translate the xAxis
        new_xAxis_x_pos = 0;
        new_xAxis_y_pos = 500 - margin['bottom_margin'];
        var translate_xAxis_by = "translate(" + new_xAxis_x_pos + ","
                        + new_xAxis_y_pos + ")";
        chart2_svg.append("g").attr("class", "axis")
                              .attr("transform", translate_xAxis_by)
                        .call(xAxis);


         chart2_svg.selectAll("rect")
             .data(feature_data)
             .enter()
             .append("rect")
              .attr("x", function(d, i) {
                        return x_axisScale(parseTime(d.year))
              })
              .attr("y", function(d, i) {
                        return y_axisScale(parseInt(d.list_price));
               })
              .attr("width", 35)
               .attr("height", function(d, i) {
                         height_scaled = y_axisScale(parseInt(d.list_price));
                         return 500 - margin['bottom_margin'] - height_scaled;  ;
                })
                .attr("fill", "steelblue");

        chart2_svg.append("text")
                  .attr("class", "x label")
                  .attr("x", dynamic_trends_div_width/2)
                  .attr("y", 430)
                  .attr("text-anchor", "middle")
                  .attr(
                        "font-size", "16px").attr(
                                      "font-family", "Helvetica").text("Year");

        //Set a label for the y-axis
            chart2_svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -5)
        .attr("x",0 - (500 / 2))
        .attr("dy", "1em")
        .attr("font-family", "Helvetica")
        .style("text-anchor", "middle")
        .text("Price");


}

function draw_barChart2(feature_data) {
    d3.select("#line_chart3").remove();
    var chart3_svg = d3.select("#chart3_dummy_svg").append("svg");
	chart3_svg.attr("width", dynamic_trends_div_width)
		  .attr("id", "line_chart3")
		  .attr("height", 500);

    var margin = {}
    margin['left_margin'] = 10
    margin['right_margin'] = 10
    margin['top_margin'] = 100
    margin['bottom_margin'] = 100

    chart3_svg.append("text")
                      .attr("x", dynamic_trends_div_width/2)
                      .attr("y", margin['top_margin']/2)
                      .attr("text-anchor", "middle")
                      .attr("font-size", "16px")
                      .text("Bar chart (multiFamilyResidenceRental)")


	min_year = d3.min(feature_data, function(d) {
                return parseTime(d.year);
        });
    max_year = d3.max(feature_data, function(d) {
                return parseTime(d.year);
        });

    min_price = d3.min(feature_data, function(d) {
                return parseInt(d.list_price);
        });
    max_price = d3.max(feature_data, function(d) {
                return parseInt(d.list_price);
        });


     var y_axisScale = d3.scaleLinear()
                                  .domain([0, max_price])
                                  .range([500 - margin['bottom_margin'], margin['top_margin']]);

                   var yAxis = d3.axisLeft()
                                 .scale(y_axisScale);

                   y_val = 500 - margin['bottom_margin']

                   var translate_yAxis_by = "translate(40,0)";
                   chart3_svg.append("g")
                      .attr("class", "axis")
                      .attr("transform", translate_yAxis_by)
                      .call(yAxis);



    //Draw x axis

    var x_axisScale = d3.scaleTime()
                                  .domain([min_year, max_year])
                                  .range([40, dynamic_trends_div_width - 100]);

    var xAxis = d3.axisBottom(x_axisScale);

        // Translate the xAxis
        new_xAxis_x_pos = 0;
        new_xAxis_y_pos = 500 - margin['bottom_margin'];
        var translate_xAxis_by = "translate(" + new_xAxis_x_pos + ","
                        + new_xAxis_y_pos + ")";
        chart3_svg.append("g").attr("class", "axis")
                              .attr("transform", translate_xAxis_by)
                        .call(xAxis);


         chart3_svg.selectAll("rect")
             .data(feature_data)
             .enter()
             .append("rect")
              .attr("x", function(d, i) {
                        return x_axisScale(parseTime(d.year))
              })
              .attr("y", function(d, i) {
                        return y_axisScale(parseInt(d.list_price));
               })
              .attr("width", 35)
               .attr("height", function(d, i) {
                         height_scaled = y_axisScale(parseInt(d.list_price));
                         return 500 - margin['bottom_margin'] - height_scaled;  ;
                })
                .attr("fill", "steelblue");

        chart3_svg.append("text")
                  .attr("class", "x label")
                  .attr("x", dynamic_trends_div_width/2)
                  .attr("y", 430)
                  .attr("text-anchor", "middle")
                  .attr(
                        "font-size", "16px").attr(
                                      "font-family", "Helvetica").text("Year");

        //Set a label for the y-axis
            chart3_svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", -5)
        .attr("x",0 - (500 / 2))
        .attr("dy", "1em")
        .attr("font-family", "Helvetica")
        .style("text-anchor", "middle")
        .text("Price");


}

function formatTick(d) {
  const s = (d / 1e5).toFixed(1);
  return this.parentNode.nextSibling ? `\xa0${s}` : `$${s} million`;
}
