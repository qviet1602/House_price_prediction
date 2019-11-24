var states_div_width = 250;
var states_div_height = 600;
var dynamic_trends_div_width = 700;
var chart_height = 300;
var states_bar_height = 50;
var parseTime = d3.timeParse("%Y");
var left_margin = 60;
var bottom_margin = 60;
var promises = [
  d3.json('/api/list_counties_purchase/'),
  d3.json('/api/county_data_rental/'),
];

Promise.all(promises).then(ready);
var global_state_data = []
function ready([state_list, state_data]) {
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
    	   .text(function(d) { return d['name']; }); 
	
	//Draw line chart here given this data
        draw_lineChart1(state_data);
        draw_lineChart2(state_data);
        draw_barChart(state_data);
	all_rectangles = d3.selectAll("rect");
        all_rectangles.each(function(d, i) {
		if(d['name'] != null && d['id'] != null && d['id'] == 1) {
                	d3.select(this).style("fill", "green");
		}
        })
}

function handleStateClick(d) {
	all_rectangles = d3.selectAll("rect");
	all_rectangles.each(function(d, i) { 
		d3.select(this).style("fill", "steelblue");
	})
	clicked_state_id = d['id'] 
	d3.select(this).style("fill", "green");
	d3.select("#line_chart1").remove();
	d3.select("#line_chart2").remove();
	d3.select("#line_chart3").remove();
	
	var state_promise = [
  		d3.json('/api/county_data_rental/?county_id=' + clicked_state_id),
	];

	Promise.all(state_promise).then(state_data_ready);
}

function state_data_ready([state_data]) {
	//Draw line chart here given this data
	draw_lineChart1(state_data);
	draw_lineChart2(state_data);
	draw_barChart(state_data);
}

function draw_lineChart1(state_data) {
	condoCoOp_data = state_data[0]['condoCoOp']
	oneBedroom_data = state_data[1]['oneBedroom']
	twoBedroom_data = state_data[2]['twoBedroom']
	threeBedroom_data = state_data[3]['threeBedroom']
	
	min_condoCoOp_year = d3.min(condoCoOp_data, function(d) {
                return parseTime(d.year);
        });

	min_oneBedroom_year = d3.min(oneBedroom_data, function(d) {
                return parseTime(d.year);
        });
	min_twoBedroom_year = d3.min(twoBedroom_data, function(d) {
                return parseTime(d.year);
        });
	min_threeBedroom_year = d3.min(threeBedroom_data, function(d) {
                return parseTime(d.year);
        });
	
	min_condoCoOp_price = d3.min(condoCoOp_data, function(d) {
                return parseInt(d.list_price);
        });

        min_oneBedroom_price = d3.min(oneBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        min_twoBedroom_price = d3.min(twoBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        min_threeBedroom_price = d3.min(threeBedroom_data, function(d) {
                return parseInt(d.list_price);
        });

	chart1_all_min_years = []
	
	chart1_all_min_years.push(min_condoCoOp_year);
	chart1_all_min_years.push(min_oneBedroom_year);
	chart1_all_min_years.push(min_twoBedroom_year);
	chart1_all_min_years.push(min_threeBedroom_year);

	min_year = d3.min(chart1_all_min_years);

	chart1_all_min_prices = []
	
	chart1_all_min_prices.push(min_condoCoOp_price);
	chart1_all_min_prices.push(min_oneBedroom_price);
	chart1_all_min_prices.push(min_twoBedroom_price);
	chart1_all_min_prices.push(min_threeBedroom_price);

	min_price = d3.min(chart1_all_min_prices);

	max_condoCoOp_year = d3.max(condoCoOp_data, function(d) {
                return parseTime(d.year);
        });

        max_oneBedroom_year = d3.max(oneBedroom_data, function(d) {
                return parseTime(d.year);
        });
        max_twoBedroom_year = d3.max(twoBedroom_data, function(d) {
                return parseTime(d.year);
        });
        max_threeBedroom_year = d3.max(threeBedroom_data, function(d) {
                return parseTime(d.year);
        });

	max_condoCoOp_price = d3.max(condoCoOp_data, function(d) {
                return parseInt(d.list_price);
        });

        max_oneBedroom_price = d3.max(oneBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        max_twoBedroom_price = d3.max(twoBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        max_threeBedroom_price = d3.max(threeBedroom_data, function(d) {
                return parseInt(d.list_price);
        });

	chart1_all_max_years = []

        chart1_all_max_years.push(max_condoCoOp_year);
        chart1_all_max_years.push(max_oneBedroom_year);
        chart1_all_max_years.push(max_twoBedroom_year);
        chart1_all_max_years.push(max_threeBedroom_year);

        max_year = d3.max(chart1_all_max_years);
	

        chart1_all_max_prices = []
        
        chart1_all_max_prices.push(max_condoCoOp_price);
        chart1_all_max_prices.push(max_oneBedroom_price);
        chart1_all_max_prices.push(max_twoBedroom_price);
        chart1_all_max_prices.push(max_threeBedroom_price);

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
                        [ min_price, max_price ]).range(
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
        var colorScheme = {'condo': '#FFC300', 'oneBedroom': '#FF5733', 'twoBedroom': '#C70039', 'threeBedroom': '#900C3F'}
	


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
                          .datum(condoCoOp_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['condo']);
	
         chart1_svg.append("path")
                          .datum(oneBedroom_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['oneBedroom']); 
	
	chart1_svg.append("path")
                          .datum(twoBedroom_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['twoBedroom']); 

	 chart1_svg.append("path")
                          .datum(threeBedroom_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['threeBedroom']); 
	
	
	//Draw the legend
        var legend_names = ['condo', 'oneBedroom', 'twoBedroom','threeBedroom']
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

function draw_lineChart2(state_data) {
	fourBedroom_data = state_data[4]['fourBedroom']
	fivePlusBedroom_data = state_data[5]['fivePlusBedroom']
	singleFamilyHome_data = state_data[6]['singleFamilyResidenceRental']

	min_fourBedroom_year = d3.min(fourBedroom_data, function(d) {
                return parseTime(d.year);
        });

	min_fivePlusBedroom_year = d3.min(fivePlusBedroom_data, function(d) {
                return parseTime(d.year);
        });
	min_singleFamilyHome_year = d3.min(singleFamilyHome_data, function(d) {
                return parseTime(d.year);
        });

	min_fourBedroom_price = d3.min(fourBedroom_data, function(d) {
                return parseInt(d.list_price);
        });

        min_fivePlusBedroom_price = d3.min(fivePlusBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        min_singleFamilyHome_price = d3.min(singleFamilyHome_data, function(d) {
                return parseInt(d.list_price);
        });

	chart2_all_min_years = []

	chart2_all_min_years.push(min_fourBedroom_year);
	chart2_all_min_years.push(min_fivePlusBedroom_year);
	chart2_all_min_years.push(min_singleFamilyHome_year);


	min_year = d3.min(chart2_all_min_years);

	chart2_all_min_prices = []

	chart2_all_min_prices.push(min_fourBedroom_price);
	chart2_all_min_prices.push(min_fivePlusBedroom_price);
	chart2_all_min_prices.push(min_singleFamilyHome_price);

	min_price = d3.min(chart2_all_min_prices);

	max_fourBedroom_year = d3.max(fourBedroom_data, function(d) {
                return parseTime(d.year);
        });

        max_fivePlusBedroom_year = d3.max(fivePlusBedroom_data, function(d) {
                return parseTime(d.year);
        });
        max_singleFamilyHome_year = d3.max(singleFamilyHome_data, function(d) {
                return parseTime(d.year);
        });


	max_fourBedroom_price = d3.max(fourBedroom_data, function(d) {
                return parseInt(d.list_price);
        });

        max_fivePlusBedroom_price = d3.max(fivePlusBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        max_singleFamilyHome_price = d3.max(singleFamilyHome_data, function(d) {
                return parseInt(d.list_price);
        });


	chart2_all_max_years = []

        chart2_all_max_years.push(max_fourBedroom_year);
        chart2_all_max_years.push(max_fivePlusBedroom_year);
        chart2_all_max_years.push(max_singleFamilyHome_year);


        max_year = d3.max(chart2_all_max_years);


        chart2_all_max_prices = []

        chart2_all_max_prices.push(max_fourBedroom_price);
        chart2_all_max_prices.push(max_fivePlusBedroom_price);
        chart2_all_max_prices.push(max_singleFamilyHome_price);


        max_price = d3.max(chart2_all_max_prices);

	var chart2_svg = d3.select("#chart2_dummy_svg").append("svg");
	chart2_svg.attr("width", dynamic_trends_div_width)
		  .attr("id", "line_chart2")
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
        chart2_svg.append("g").attr("class", "axis").attr("transform",
                        translate_xAxis_by).call(xAxis);

	// Draw y axis

	var y_axisScale = d3.scaleLinear().domain(
                        [ min_price, max_price ]).range(
                        [ chart_height - bottom_margin, left_margin ]);

        new_yAxis_x_pos = left_margin;
        new_yAxis_y_pos = 0;
        var translate_yAxis_by = "translate(" + new_yAxis_x_pos + ","
                        + new_yAxis_y_pos + ")";

        var yAxis = d3.axisLeft().scale(y_axisScale);

        chart2_svg.append("g").attr("class", "axis").attr("transform",
                        translate_yAxis_by).call(yAxis);

    chart2_svg.append("text").attr("class", "x label").attr("x", dynamic_trends_div_width / 2).attr("y",
                        chart_height - 20).attr("text-anchor", "middle").attr(
                        "font-size", "16px").attr(
                                        "font-family", "Helvetica").text("Year");
    //Set a label for the y-axis
        chart2_svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -5)
    .attr("x",0 - (chart_height / 2))
    .attr("dy", "1em")
    .attr("font-family", "Helvetica")
    .style("text-anchor", "middle")
    .text("Price");
	//Draw lines
	var all_colors = d3.schemeCategory10;
        var colorScheme = {'fourBedroom': all_colors[0], 'fivePlusBedroom': all_colors[1], 'singleFamilyHome': all_colors[2]}



        var line = d3.line()
                                  .x(function(d) {
                                          return x_axisScale(parseTime(d.year));
                                  })
                                  .y(function(d) {
                                          return y_axisScale(parseInt(d.list_price));
                                  })
                                  ;
	chart2_svg.append("path")
                          .datum(fourBedroom_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['fourBedroom']);

         chart2_svg.append("path")
                          .datum(fivePlusBedroom_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['fivePlusBedroom']);

	chart2_svg.append("path")
                          .datum(singleFamilyHome_data)
                          .attr("d", line)
                          .style("fill", "none")
                          .style("stroke-width", 1)
                      .style("stroke", colorScheme['singleFamilyHome']);


	//Draw the legend
        var legend_names = ['fourBedroom', 'fivePlusBedroom', 'singleFamilyHome']
        chart2_svg.selectAll("legend_rect")
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

         chart2_svg.selectAll("legend_label")
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

function draw_barChart(state_data) {
    var chart3_svg = d3.select("#chart3_dummy_svg").append("svg");
	chart3_svg.attr("width", dynamic_trends_div_width)
		  .attr("id", "line_chart3")
		  .attr("height", 400);

    condoCoOp_data = state_data[0]['condoCoOp']
	oneBedroom_data = state_data[1]['oneBedroom']
	twoBedroom_data = state_data[2]['twoBedroom']
	threeBedroom_data = state_data[3]['threeBedroom']
	fourBedroom_data = state_data[4]['fourBedroom']
	fivePlusBedroom_data = state_data[5]['fivePlusBedroom']
	singleFamilyHome_data = state_data[6]['singleFamilyResidenceRental']

	min_condoCoOp_price = d3.min(condoCoOp_data, function(d) {
                return parseInt(d.list_price);
        });

    min_oneBedroom_price = d3.min(oneBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
    min_twoBedroom_price = d3.min(twoBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
    min_threeBedroom_price = d3.min(threeBedroom_data, function(d) {
                return parseInt(d.list_price);
        });


    min_fourBedroom_price = d3.min(fourBedroom_data, function(d) {
                return parseInt(d.list_price);
        });

        min_fivePlusBedroom_price = d3.min(fivePlusBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        min_singleFamilyHome_price = d3.min(singleFamilyHome_data, function(d) {
                return parseInt(d.list_price);
        });

    chart3_all_min_prices = []

    chart3_all_min_prices.push(min_condoCoOp_price);
    chart3_all_min_prices.push(min_oneBedroom_price);
    chart3_all_min_prices.push(min_twoBedroom_price);
    chart3_all_min_prices.push(min_fourBedroom_price);
    chart3_all_min_prices.push(min_fivePlusBedroom_price);
    chart3_all_min_prices.push(min_singleFamilyHome_price);

    min_price = d3.min(chart3_all_min_prices);


    max_condoCoOp_price = d3.max(condoCoOp_data, function(d) {
                return parseInt(d.list_price);
        });

    max_oneBedroom_price = d3.max(oneBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
    max_twoBedroom_price = d3.max(twoBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
    max_threeBedroom_price = d3.max(threeBedroom_data, function(d) {
                return parseInt(d.list_price);
        });


    max_fourBedroom_price = d3.max(fourBedroom_data, function(d) {
                return parseInt(d.list_price);
        });

        max_fivePlusBedroom_price = d3.max(fivePlusBedroom_data, function(d) {
                return parseInt(d.list_price);
        });
        max_singleFamilyHome_price = d3.max(singleFamilyHome_data, function(d) {
                return parseInt(d.list_price);
        });

    chart3_all_max_prices = []

    chart3_all_max_prices.push(max_condoCoOp_price);
    chart3_all_max_prices.push(max_oneBedroom_price);
    chart3_all_max_prices.push(max_twoBedroom_price);
    chart3_all_max_prices.push(max_fourBedroom_price);
    chart3_all_max_prices.push(max_fivePlusBedroom_price);
    chart3_all_max_prices.push(max_singleFamilyHome_price);

    max_price = d3.max(chart3_all_max_prices);

    //Draw x axis
    /*var x_axisScale = d3.scaleBand()
                      .domain(['condoCoOp', 'oneBedroom', 'twoBedroom', 'threeBedroom', 'fourBedroom', 'fivePlusBedroom'])
					  .padding(0.1)
					  .rangeRound(
                        [ left_margin, dynamic_trends_div_width - left_margin ]);

        var tick_size = dynamic_trends_div_width - left_margin;
        var xAxis = d3.axisBottom(x_axisScale)
                      .tickSize(-280)
                      .tickSizeOuter(0);

        // Translate the xAxis
        new_xAxis_x_pos = 0;
        new_xAxis_y_pos = 400 - bottom_margin;
        var translate_xAxis_by = "translate(" + new_xAxis_x_pos + ","
                        + new_xAxis_y_pos + ")";
        chart3_svg.append("g").attr("class", "axis").attr("transform",
                        translate_xAxis_by)
                        .call(xAxis)
                        .selectAll("text")
    //.attr("transform", "translate(-10,10)rotate(-45)")
    .style("text-anchor", "start")
    .style("font-size", 20)
    .style("fill", "#69a3b2"); */

    //Draw y axis
    var y_axisScale = d3.scaleLinear()

                    .domain([0, max_price])
                    .range([400 - bottom_margin, 0]);

    chart3_svg
        .attr("transform", `translate(0,0)`)
        .call(d3.axisRight(y_axisScale)
        .tickSize(dynamic_trends_div_width)
        )
        .call(g => g.select(".domain")
        .remove())
        .call(g => g.selectAll(".tick:not(:first-of-type) line")
        .attr("stroke-opacity", 0.5)
        .attr("stroke-dasharray", "2,2"))
        .call(g => g.selectAll(".tick text")
        .attr("x", 4)
        .attr("dy", -4));

    //Draw x axis
    home_types = ['condoCoOp', 'oneBedroom', 'twoBedroom', 'threeBedroom', 'fourBedroom', 'fivePlusBedroom']
    var x_axisScale = d3.scaleBand()
	.range([0, dynamic_trends_div_width - 100])
	.domain(home_types);





    /*var y_axisScale = d3.scaleLinear()
                      .domain([min_price, max_price])
					  .rangeRound(
                        [ 400 - bottom_margin, left_margin ]);

        new_yAxis_x_pos = left_margin;
        new_yAxis_y_pos = 0;
        var translate_yAxis_by = "translate(" + new_yAxis_x_pos + ","
                        + new_yAxis_y_pos + ")";

        var yAxis = d3.axisLeft().scale(y_axisScale);

        chart3_svg.append("g").attr("class", "axis").attr("transform",
                        translate_yAxis_by).call(yAxis); */

        var xAxis = d3.axisBottom(x_axisScale)
                      .tickSize(-400)
                      .tickSizeOuter(0);

        // Translate the xAxis
        new_xAxis_x_pos = 0;
        new_xAxis_y_pos = 400 - bottom_margin;
        var translate_xAxis_by = "translate(" + new_xAxis_x_pos + ","
                        + new_xAxis_y_pos + ")";
        chart3_svg.append("g").attr("class", "axis").attr("transform",
                        translate_xAxis_by).call(xAxis)
                        .selectAll("text")
    //.attr("transform", "translate(-10,10)rotate(-45)")
    .style("text-anchor", "start")
    .style("font-size", 20)
    .style("fill", "#69a3b2");

        //Draw the bar chart
        condoCoOp_data_last_5years = []
        oneBedroom_data_last_5years = []
        twoBedroom_data_last_5years = []
        threeBedroom_data_last_5years = []
        fourBedroom_data_last_5years = []
        fivePlusBedroom_data_last_5years = []

        all_years = ['2015', '2016', '2017', '2018', '2019']

        for(var k =0; k<all_years.length; k++) {
            current_year = all_years[k]
            current_year_data = null;
            for(var i=0; i<condoCoOp_data.length; i++) {
                each_year_data = condoCoOp_data[i]
                year = parseInt(each_year_data.year)
                if(year == current_year) {
                    current_year_data = each_year_data
                }
            }
            if(current_year_data != null) {
                current_dict = {}
                current_dict['year'] = current_year_data.year
                current_dict['list_price'] = current_year_data.list_price;
                condoCoOp_data_last_5years.push(current_dict)
            } else {
                current_dict = {}
                current_dict['year'] = parseInt(current_year)
                current_dict['list_price'] = 0;
                condoCoOp_data_last_5years.push(current_dict)
            }

            current_year_data = null;
            for(var i=0; i<oneBedroom_data.length; i++) {
                each_year_data = oneBedroom_data[i]
                year = parseInt(each_year_data.year)
                if(year == current_year) {
                    current_year_data = each_year_data
                }
            }

            if(current_year_data != null) {
                current_dict = {}
                current_dict['year'] = current_year_data.year
                current_dict['list_price'] = current_year_data.list_price;
                oneBedroom_data_last_5years.push(current_dict)
            } else {
                current_dict = {}
                current_dict['year'] = parseInt(current_year)
                current_dict['list_price'] = 0;
                oneBedroom_data_last_5years.push(current_dict)
            }

            current_year_data = null;
            for(var i=0; i<twoBedroom_data.length; i++) {
                each_year_data = twoBedroom_data[i]
                year = parseInt(each_year_data.year)
                if(year == current_year) {
                    current_year_data = each_year_data
                }
            }

            if(current_year_data != null) {
                current_dict = {}
                current_dict['year'] = current_year_data.year
                current_dict['list_price'] = current_year_data.list_price;
                twoBedroom_data_last_5years.push(current_dict)
            } else {
                current_dict = {}
                current_dict['year'] = parseInt(current_year)
                current_dict['list_price'] = 0;
                twoBedroom_data_last_5years.push(current_dict)
            }

            current_year_data = null;
            for(var i=0; i<threeBedroom_data.length; i++) {
                each_year_data = threeBedroom_data[i]
                year = parseInt(each_year_data.year)
                if(year == current_year) {
                    current_year_data = each_year_data
                }
            }

            if(current_year_data != null) {
                current_dict = {}
                current_dict['year'] = current_year_data.year
                current_dict['list_price'] = current_year_data.list_price;
                threeBedroom_data_last_5years.push(current_dict)
            } else {
                current_dict = {}
                current_dict['year'] = parseInt(current_year)
                current_dict['list_price'] = 0;
                threeBedroom_data_last_5years.push(current_dict)
            }

            current_year_data = null;
            for(var i=0; i<fourBedroom_data.length; i++) {
                each_year_data = fourBedroom_data[i]
                year = parseInt(each_year_data.year)
                if(year == current_year) {
                    current_year_data = each_year_data
                }
            }

            if(current_year_data != null) {
                current_dict = {}
                current_dict['year'] = current_year_data.year
                current_dict['list_price'] = current_year_data.list_price;
                fourBedroom_data_last_5years.push(current_dict)
            } else {
                current_dict = {}
                current_dict['year'] = parseInt(current_year)
                current_dict['list_price'] = 0;
                fourBedroom_data_last_5years.push(current_dict)
            }

            current_year_data = null;
            for(var i=0; i<fivePlusBedroom_data.length; i++) {
                each_year_data = fivePlusBedroom_data[i]
                year = parseInt(each_year_data.year)
                if(year == current_year) {
                    current_year_data = each_year_data
                }
            }

            if(current_year_data != null) {
                current_dict = {}
                current_dict['year'] = current_year_data.year
                current_dict['list_price'] = current_year_data.list_price;
                fivePlusBedroom_data_last_5years.push(current_dict)
            } else {
                current_dict = {}
                current_dict['year'] = parseInt(current_year)
                current_dict['list_price'] = 0;
                fivePlusBedroom_data_last_5years.push(current_dict)
            }
        }


        var colors = d3.schemeCategory10;

        var colorScheme = {'2015': colors[0], '2016': colors[1],
                        '2017': colors[2], '2018' : colors[3], '2019' : colors[4]}

        each_band_section = x_axisScale.bandwidth()/5
        last_x_value = 0

        chart3_svg.selectAll(".condoCoOpbar")
                   .data(condoCoOp_data_last_5years)
                   .enter().append("rect")
                   .attr("class", "condoCoOpbar")
                   .attr("x", function(d, i) {
                        x_val = left_margin - 10 + i * each_band_section;
                        last_x_value = x_val
                        return x_val;
                   })
                   .attr("y", function(d) {
                            return y_axisScale(parseInt(d.list_price));
                   })
                   .attr("width", function(d) {
                           return each_band_section - 1;
                   } )
                   .attr("height", function(d) {
                        if(d.list_price == 0) {
                            return 0;
                        } else {
                            height_scaled = y_axisScale(parseInt(d.list_price));
                            return 400 - bottom_margin - height_scaled;
                        }

                   })
                   .style("fill", function(d) {
                        year = d.year;
                        return colorScheme[year];
                   });

        oneBedroom_last_x_value = 0
        chart3_svg.selectAll(".oneBedroombar")
                   .data(oneBedroom_data_last_5years)
                   .enter().append("rect")
                   .attr("class", "oneBedroombar")
                   .attr("x", function(d, i) {
                        x_val = last_x_value + each_band_section + i * each_band_section;
                        oneBedroom_last_x_value = x_val;
                        return x_val;
                   })
                   .attr("y", function(d) {
                            return y_axisScale(parseInt(d.list_price));
                   })
                   .attr("width", function(d) {
                           return each_band_section - 1;
                   } )
                   .attr("height", function(d) {
                        if(d.list_price == 0) {
                            return 0;
                        } else {
                            height_scaled = y_axisScale(parseInt(d.list_price));
                            return 400 - bottom_margin - height_scaled;
                        }

                   })
                   .style("fill", function(d) {
                        year = d.year;
                        return colorScheme[year];
                   });

        twoBedroom_last_x_value = 0;
        chart3_svg.selectAll(".twoBedroombar")
                   .data(twoBedroom_data_last_5years)
                   .enter().append("rect")
                   .attr("class", "twoBedroombar")
                   .attr("x", function(d, i) {
                        x_val = oneBedroom_last_x_value + each_band_section + i * each_band_section;
                        twoBedroom_last_x_value = x_val;
                        return x_val;
                   })
                   .attr("y", function(d) {
                            return y_axisScale(parseInt(d.list_price));
                   })
                   .attr("width", function(d) {
                           return each_band_section - 1;
                   } )
                   .attr("height", function(d) {
                        if(d.list_price == 0) {
                            return 0;
                        } else {
                            height_scaled = y_axisScale(parseInt(d.list_price));
                            return 400 - bottom_margin - height_scaled;
                        }
                   })
                   .style("fill", function(d) {
                        year = d.year;
                        return colorScheme[year];
                   });

        threeBedroom_last_x_value = 0;
        chart3_svg.selectAll(".threeBedroombar")
                   .data(threeBedroom_data_last_5years)
                   .enter().append("rect")
                   .attr("class", "threeBedroombar")
                   .attr("x", function(d, i) {
                        x_val = twoBedroom_last_x_value + each_band_section + i * each_band_section;
                        threeBedroom_last_x_value = x_val;
                        return x_val;
                   })
                   .attr("y", function(d) {
                            return y_axisScale(parseInt(d.list_price));
                   })
                   .attr("width", function(d) {
                           return each_band_section - 1;
                   } )
                   .attr("height", function(d) {
                        if(d.list_price == 0) {
                            return 0;
                        } else {
                            height_scaled = y_axisScale(parseInt(d.list_price));
                            return 400 - bottom_margin - height_scaled;
                        }
                   })
                   .style("fill", function(d) {
                        year = d.year;
                        return colorScheme[year];
                   });

        fourBedroom_last_x_value = 0;
        chart3_svg.selectAll(".fourBedroombar")
                   .data(fourBedroom_data_last_5years)
                   .enter().append("rect")
                   .attr("class", "fourBedroombar")
                   .attr("x", function(d, i) {
                        x_val = threeBedroom_last_x_value + each_band_section + i * each_band_section;
                        fourBedroom_last_x_value = x_val;
                        return x_val;
                   })
                   .attr("y", function(d) {
                            return y_axisScale(parseInt(d.list_price));
                   })
                   .attr("width", function(d) {
                           return each_band_section - 1;
                   } )
                   .attr("height", function(d) {
                        if(d.list_price == 0) {
                            return 0;
                        } else {
                            height_scaled = y_axisScale(parseInt(d.list_price));
                            return 400 - bottom_margin - height_scaled;
                        }

                   })
                   .style("fill", function(d) {
                        year = d.year;
                        return colorScheme[year];
                   });

        fiveBedroom_last_x_value = 0;
        chart3_svg.selectAll(".fiveBedroombar")
                   .data(fivePlusBedroom_data_last_5years)
                   .enter().append("rect")
                   .attr("class", "fiveBedroombar")
                   .attr("x", function(d, i) {
                        x_val = fourBedroom_last_x_value + each_band_section + i * each_band_section;
                        fiveBedroom_last_x_value = x_val;
                        return x_val;
                   })
                   .attr("y", function(d) {
                            return y_axisScale(parseInt(d.list_price));
                   })
                   .attr("width", function(d) {
                           return each_band_section - 1;
                   } )
                   .attr("height", function(d) {
                        if(d.list_price == 0) {
                            return 0;
                        } else {
                            height_scaled = y_axisScale(parseInt(d.list_price));
                            return 400 - bottom_margin - height_scaled;
                        }

                   })
                   .style("fill", function(d) {
                        year = d.year;
                        return colorScheme[year];
                   });


        //Draw the legend
        var legend_names = ['2015', '2016', '2017','2018', '2019']
        chart3_svg.selectAll("legend_rect")
                          .data(legend_names)
                          .enter()
                          .append("rect")
                          .attr("x", function(d, i) {
                            return 50 + (i * 20);
                          })
                          .attr("y", function(d, i) {
                                  return 400;
                          })
                          .attr("width", 20)
                          .attr("height", 20)
                          .style("fill", function(d) {
                                  return colorScheme[d];
                          });


    var chart4_svg = d3.select("#chart4_dummy_svg").append("svg");
	chart4_svg.attr("width", dynamic_trends_div_width)
		  .attr("id", "line_chart4")
		  .attr("height", 200);

    var legend_names = ['2015', '2016', '2017','2018', '2019']
        chart4_svg.selectAll("legend_rect")
                          .data(legend_names)
                          .enter()
                          .append("rect")
                          .attr("x", function(d, i) {
                            return 50 + (i * 100);
                          })
                          .attr("y", function(d, i) {
                                  return 0;
                          })
                          .attr("width", 10)
                          .attr("height", 10)
                          .style("fill", function(d) {
                                  return colorScheme[d];
                          });

    chart4_svg.selectAll("legend_label")
          .data(legend_names)
          .enter()
          .append("text")
          .attr("x", function(d, i) {
            return 70 + (i * 100);
          })
          .attr("y", function(d, i) {
                  return 12;
          })
          .attr("width", 30)
          .attr("height", 30)
          .attr("text-anchor", "left")
          .attr("font-family", "Helvetica")
          .text(function(d){ return d})
          .style("fill", function(d) {
                  return colorScheme[d];
          })
          .style("alignment-baseline", "middle");

}

function formatTick(d) {
  const s = (d / 1e5).toFixed(1);
  return this.parentNode.nextSibling ? `\xa0${s}` : `$${s} million`;
}
