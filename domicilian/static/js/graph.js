var menuWidth = 200;
var menuItemHeight = 50;
var menuOffset = 60;

var rightClickMenuItemHeight = 40;
var createdNodes = {};
var totalNodes = 0;
var colors = d3.schemeCategory10;
var nodeGroups = [0, 1, 2];
var nodeColors = [d3.schemeBlues[5], d3.schemeOranges[5], d3.schemeGreens[5]];
var countyNodes = {
  best: {},
  zip: {},
  safe: {},
  affordable: {}
};

var svg = d3.select('svg');
var width = parseInt(svg.style('width'));
var usStates = []
var promises = [
  d3.json('/api/list_states/'),
];
var height = parseInt(svg.style('height'))

var graph = {
  nodes: [],
  links: []
};

var simulation = d3.forceSimulation()
  .force('link', d3.forceLink().id(function (d) { return d.id; }).distance(200))
  .force('charge', d3.forceManyBody().strength(-30))
  // .force('center', d3.forceCenter(500, 500))

var links = svg.append('g')
  .attr('class', 'links');

var nodes = svg.append('g')
  .attr('class', 'nodes');

Promise.all(promises).then(ready);
function ready([state_list]) {
  usStates = state_list;

  var menu = svg.append('g')
    .attr('class', 'menu');

  // Adjust nodes, labels, and lines on scroll to remain in view at all times
  // This allows the user to scroll through the state list without losing their existing nodes
  d3.select(window).on('scroll', function () {
    removeRightClickMenu();
    removeStatBox();

    simulation.restart();
  })

  createMenu(menu, usStates);

  var legend = svg.append('g')
    .attr('class', 'legend')

  createLegend(legend);
}

/**
* List of main functions and brief description
*
* createMenu() => Displays the list of states on the right side and sets up handlers and interactions
*                 This is the only function that runs on initial page load
* createForceStateNode() => Creates a node for a state at the location the user drags to
*                      Enables right click menu creation on user right click
* createRightClickMenu() => Displays right click menu for node
* createForceCountyNodes() => Creates county nodes and links them to a given state
*/
// Create entire right side state menu including clear all button
function createMenu(menu, usStates) {
  // 'Clear and Start Over' button
  menu.append('rect')
    .attr('class', 'clear-all hidden')
    .attr('height', rightClickMenuItemHeight)
    .attr('width', menuWidth - 20)
    .attr('y', 5)
    .attr('x', width - menuWidth - 10)
    .attr('fill', 'rgb(81, 116 ,187)')
    .attr('stroke', 'rgb(57, 83, 137)')
    .attr('stroke-width', 2)
    .on('mousedown', function () { d3.select(this).classed('active', true) })
    .on('mouseup', function () {
      d3.select(this).classed('active', false);
      deleteAllNodes();
    });

  // 'Clear and Start Over' label
  menu.append('text')
    .attr('class', 'clear-all-label hidden')
    .attr('y', 30)
    .attr('x', width - 120)
    .attr('font-size', '15px')
    .attr('fill', 'white')
    .attr('text-anchor', 'middle')
    .attr('font-weight', 'bold')
    .text('Clear and Start Over')
    .on('mousedown', function () { d3.select(this).classed('active', true) })
    .on('mouseup', function () {
      d3.select(this).classed('active', false);
      deleteAllNodes();
    });

  // State name menu items
  menu.selectAll('.menu-item')
    .data(usStates)
    .enter().append('rect')
    .attr('class', function (state) { return genClassName(state['name']) + '-menu-item' + ' menu-item' })
    .attr('height', 50)
    .attr('width', menuWidth)
    .attr('y', function (d, i) { return i * menuItemHeight + menuOffset })
    .attr('x', width - menuWidth - 20)
    .attr('fill', 'rgb(81, 116 ,187)')
    .attr('stroke', 'rgb(57, 83, 137)')
    .attr('stroke-width', 2)
    .call(d3.drag()
      .on('start', menuOnDragStart)
      .on('end', menuOnDragEnd))

  // State name menu labels
  menu.selectAll('.menu-item-label')
    .data(usStates)
    .enter().append('text')
    .attr('class', 'menu-item-label')
    .attr('y', function (d, i) { return i * menuItemHeight + 90 })
    .attr('x', width - menuWidth / 2 - 20)
    .attr('font-size', '17px')
    .attr('fill', 'white')
    .attr('text-anchor', 'middle')
    .attr('font-weight', 'bold')
    .text(function (d) { return d['name'] })
    .call(d3.drag()
      .on('start', menuOnDragStart)
      .on('end', menuOnDragEnd))

  // Menu item drag start function
  function menuOnDragStart(d) {
    removeRightClickMenu();

    if (createdNodes[d['name']] === undefined && totalNodes < 3) {
      d3.select('.' + genClassName(d['name']) + '-menu-item').attr('fill', nodeColors[nodeGroups[0]][2]);
    }

    d3.select(this).classed('active', true);
    d3.select('.' + d['name'] + '-node');
  }

  // Menu item drag end function
  function menuOnDragEnd(d) {
    d3.select(this).classed('active', false);
    if (d3.event.x >= 1030) {
      createForceStateNode(d, d3.event.x - 300);
    } else {
      createForceStateNode(d);
    }
  }
}

// Right click menu options
var menuOptions = [
  'Drag Similar States',
  'Show 5 Best Counties',
  'Show 5 Best Zip Codes',
  'Show 5 Safe Counties',
  'Show 5 Affordable Counties',
  'Show All',
  'Delete State',
  'Select All for All Similar States'
];

// Right click menu functions
var menuFunctions = [
  dragSimilarStates,
  showBestCounties,
  showBestZipCodes,
  showSafeCounties,
  showAffordableCounties,
  showAll,
  deleteState,
  selectAllForAllSimilarStates
];

// TODO: Remove this option when more than one state node exists
function dragSimilarStates(stateName) {
  if (totalNodes === 1) {
    d3_event_x = d3.event.x
    d3_event_y = d3.event.y
    d3.json('/api/similar_states/?state_name=' + stateName)
      .then(function (data) {
        for (var i = 0; i < data.length - 1; i++) {
          each_state = data[i]
          createForceStateNode(each_state, d3_event_x + i * 5, d3_event_y + i * 100);
          d3.select('.' + genClassName(each_state['name']) + '-menu-item').attr('fill', nodeColors[i + 1][2]);

        }

        removeRightClickMenu();
      });
  }
}

function showBestCounties(stateName) {
  if (countyNodes.best[stateName]) {
    removeRightClickMenu();
    return;
  }

  countyNodes.best[stateName] = true;

  d3.json('/api/best_counties/?state_name=' + stateName)
    .then(function (data) {
      createForceCountyNodes(stateName, data, 0)
    });
}

function showBestZipCodes(stateName) {
  if (countyNodes.zip[stateName]) {
    removeRightClickMenu();
    return;
  }

  countyNodes.zip[stateName] = true;

  d3.json('/api/best_zips/?state_name=' + stateName)
    .then(function (data) {
      createForceCountyNodes(stateName, data, 1);
    });
}

function showSafeCounties(stateName) {
  if (countyNodes.safe[stateName]) {
    removeRightClickMenu();
    return;
  }

  countyNodes.safe[stateName] = true;

  d3.json('/api/safe_counties/?state_name=' + stateName)
    .then(function (data) {
      createForceCountyNodes(stateName, data, 3);
    });
}

function showAffordableCounties(stateName) {
  if (countyNodes.affordable[stateName]) {
    removeRightClickMenu();
    return;
  }

  countyNodes.affordable[stateName] = true;

  d3.json('/api/affordable/?state_name=' + stateName)
    .then(function (data) {
      createForceCountyNodes(stateName, data, 4);
    });
}

function showAll(stateName, callback) {
  d3.json('/api/all_data/?state_name=' + stateName)
    .then(function (data) {
      best_counties = data['best_counties']
      safe_counties = data['safe_counties']
      affordable_counties = data['affordable_counties']
      best_zips = data['best_zips']

      if (!countyNodes.best[stateName]) {
        countyNodes.best[stateName] = true;
        createForceCountyNodes(stateName, best_counties, 0);
      }

      if (!countyNodes.zip[stateName]) {
        countyNodes.zip[stateName] = true;
        createForceCountyNodes(stateName, best_zips, 1);
      }

      if (!countyNodes.safe[stateName]) {
        countyNodes.safe[stateName] = true;
        createForceCountyNodes(stateName, safe_counties, 3);
      }

      if (!countyNodes.affordable[stateName]) {
        countyNodes.affordable[stateName] = true;
        createForceCountyNodes(stateName, affordable_counties, 4);
      }

      removeRightClickMenu();

      callback();
    });
}

function selectAllForAllSimilarStates(stateName) {
  var states = Object.keys(createdNodes).map(function(state) { return state });
  d3.json('/api/similar_all/?states=' + states.join('_'))
    .then(function (data) {
      count = 0;
      // Ignore this I'm tired
      showAll(states[count], function() {
        count++
        showAll(states[count], function() {
          count++
          showAll(states[count], function () {
            connectSimilarCounties(data['affordable_counties']);
            connectSimilarCounties(data['best_counties']);
            connectSimilarCounties(data['best_zips']);
            connectSimilarCounties(data['safe_counties']);
          });
        })
      });
    });
}

// Delete the state node and all children nodes
function deleteState(stateName) {
  // Resert color of state menu item
  d3.select('.' + genClassName(stateName) + '-menu-item').attr('fill', 'rgb(81, 116 ,187)');

  // Remove nodes and links associated with deleted state
  graph.links = graph.links.filter(function(link) { return link.source.id !== stateName && link.states.indexOf(stateName) === -1 });
  graph.nodes = graph.nodes.filter(function(node) { return node.id !== stateName && node.state !== stateName });

  var node = nodes.selectAll('.node').data(graph.nodes, function(d) { return d.id });
  node.exit().remove();

  var link = links.selectAll('.link').data(graph.links, function(d) { return d.index; });
  link.exit().remove();

  simulation.restart();

  removeRightClickMenu();

  nodeGroups.push(createdNodes[stateName]);
  delete createdNodes[stateName];
  delete countyNodes.best[stateName];
  delete countyNodes.zip[stateName];
  delete countyNodes.safe[stateName];
  delete countyNodes.affordable[stateName];
  totalNodes--;

  // Remove clear all button if no more state nodes exist
  if (totalNodes === 0) {
    d3.select('.clear-all').classed('hidden', true);
    d3.select('.clear-all-label').classed('hidden', true);
  }
}

function createForceStateNode(stateObj, x, y) {
  // Return if the node already exists or there are 3 total nodes
  if (createdNodes[stateObj['name']] !== undefined || totalNodes >= 3) {
    return;
  }

  var nodeData = { id: stateObj['name'], idx: -1, group: nodeGroups[0], x: x || d3.event.x, y: y || d3.event.y - window.scrollY };
  graph.nodes.push(nodeData);

  simulation.nodes(graph.nodes)
    .on('tick', ticked);

  var link = links.selectAll('.link').data(graph.links);
  var linkEnter = link.enter().append('g')
    .attr('class', 'link')

  linkEnter
    .append("line")
    .attr("stroke", "black")
    .attr("stroke-width", function(d) {
      return Math.sqrt(d.value);
    })
    .attr("stroke-opacity", 0.3)

  link = linkEnter.merge(link);
  link.exit().remove();

  var node = nodes.selectAll('.node').data(graph.nodes);
  var nodeEnter = node.enter().append('g')
    .attr('class', 'node')

  nodeEnter
    .append("circle")
    .attr("r", "20px")
    .attr("fill", function(d) {
      return nodeColors[d.group][2];
    })
    .attr("stroke", "black")
    .attr("stroke-width", "2")
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    )
    .on("contextmenu", function() {
      d3.event.preventDefault();

      createRightClickMenu(stateObj["name"], d3.select(this));
      removeStatBox();
    })
    .on("mouseover", mouseover)
  // .on('mouseout', mouseout)

  nodeEnter
    .append("text")
    .attr("font-size", "17px")
    .attr("text-anchor", "middle")
    .attr("font-weight", "bold")
    .text(function(d) {
      return d.id;
    })

  node = nodeEnter.merge(node);
  node.exit().remove();

  simulation.restart();

  createdNodes[stateObj['name']] = nodeGroups[0];
  nodeGroups.shift();
  totalNodes++;

  // Enable clear all button
  d3.select('.clear-all').classed('hidden', false);
  d3.select('.clear-all-label').classed('hidden', false);

  function ticked() {
    link.selectAll('line')
      .attr('x1', function (d) { return d.source.x; })
      .attr('y1', function (d) { return d.source.y + window.scrollY; })
      .attr('x2', function (d) { return d.target.x; })
      .attr('y2', function (d) { return d.target.y + window.scrollY; });

    node.selectAll('circle')
      .attr('cx', function (d) { return d.x })
      .attr('cy', function (d) { return d.y + window.scrollY })

    node
      .selectAll("text")
      .attr("x", function(d) {
        return d.x;
      })
      .attr("y", function(d) {
        return d.y - 30 + window.scrollY;
      })
  }
}

function connectSimilarCounties(data) {
  for (var i = 0; i < data.length; i++) {
    county = data[i];
    for (var j = 0; j < county.similars.length; j++) {
      similar = county.similars[j];
      graph.links.push({ source: county['name'] + '-' + genClassName(county.state_name), target: similar['name'] + '-' + genClassName(similar.state_name), value: 2, states: [county.state_name, similar.state_name] });
    }
  }

  simulation.force('link')
    .links(graph.links);

  simulation.nodes(graph.nodes)
    .on('tick', ticked);

  var link = links.selectAll('.link').data(graph.links);
  var linkEnter = link.enter().append('g')
    .attr('class', 'link')

  linkEnter.append('line')
    .attr('stroke', 'black')
    .attr('stroke-dasharray', '10 5')
    .attr('stroke-width', function (d) { return Math.sqrt(d.value) })
    .attr('stroke-opacity', 0.7)

  link = linkEnter.merge(link);
  link.exit().remove();

  var node = nodes.selectAll('.node').data(graph.nodes);
  node.exit().remove();

  simulation.restart();

  function ticked() {
    link.selectAll('line')
      .attr('x1', function (d) { return d.source.x; })
      .attr('y1', function (d) { return d.source.y + window.scrollY; })
      .attr('x2', function (d) { return d.target.x; })
      .attr('y2', function (d) { return d.target.y + window.scrollY; });

    node.selectAll('circle')
      .attr('cx', function (d) { return d.x })
      .attr('cy', function (d) { return d.y + window.scrollY })

    node.selectAll('text')
      .attr('x', function (d) { return d.x })
      .attr('y', function (d) { return d.y - 30 + window.scrollY })
  }
}

function createForceCountyNodes(stateName, data, colorShade) {
  for (var i = 0; i < data.length; i++) {
    each = data[i]

    var stateObj = graph.nodes.find(function(node) { return node.id === stateName });
    graph.nodes.push({ id: each['name'].trim() + '-' + genClassName(stateName), name: each['name'], idx: each['id'], group: createdNodes[stateName], x: stateObj.x - 100 + 50 * i , y: stateObj.y + 100, state: stateName })
    graph.links.push({ source: stateName, target: each['name'].trim() + '-' + genClassName(stateName), value: 2, states: [] })
  }

  simulation.force('link')
    .links(graph.links);

  simulation.nodes(graph.nodes)
    .on('tick', ticked);

  var link = links.selectAll('.link').data(graph.links);
  var linkEnter = link.enter().append('g')
    .attr('class', 'link')

  linkEnter
    .append("line")
    .attr("stroke", "black")
    .attr("stroke-width", function(d) {
      return Math.sqrt(d.value);
    })
    .attr("stroke-opacity", 0.3)

  link = linkEnter.merge(link);
  link.exit().remove();

  var node = nodes.selectAll('.node').data(graph.nodes);
  var nodeEnter = node.enter().append('g')
    .attr('class', 'node')

  nodeEnter
    .append("circle")
    .attr("r", "15px")
    .attr("fill", function(d) {
      return nodeColors[createdNodes[stateName]][colorShade];
    })
    .attr("stroke", "black")
    .attr("stroke-width", 2)
    .call(
      d3
        .drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    )
    .on("mouseover", mouseover)
  // .on('mouseout', mouseout)

  nodeEnter
    .append("text")
    .attr("font-size", "15px")
    .attr("text-anchor", "middle")
    .attr("font-weight", "bold")
    .text(function(d) {
      return d.name;
    })

  node = nodeEnter.merge(node);
  node.exit().remove();

  simulation.restart();

  removeRightClickMenu();

  function ticked() {
    link.selectAll('line')
      .attr('x1', function (d) { return d.source.x; })
      .attr('y1', function (d) { return d.source.y + window.scrollY; })
      .attr('x2', function (d) { return d.target.x; })
      .attr('y2', function (d) { return d.target.y + window.scrollY; });

    node.selectAll('circle')
      .attr('cx', function (d) { return d.x })
      .attr('cy', function (d) { return d.y + window.scrollY })

    node.selectAll('text')
      .attr('x', function (d) { return d.x })
      .attr('y', function (d) { return d.y - 30 + window.scrollY })
  }
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;

  removeRightClickMenu();
  removeStatBox();
  d3.select(this).classed('active', true);
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
  d3.select(this).classed('active', false);
}

function mouseover(d) {
  if (!d3.select('.right-click-menu').empty() || d3.select(this).classed('active')) {
    return;
  }

  node_type = 'state';
  node_id = d['id'];
  if (d['idx'] > 0) {
    node_type = 'county'
    node_id = d['idx']
  }

  var x = d.x + 10
  var y = d.y + window.scrollY + 10
  node_data = node_type + '_' + node_id
  d3.json('/api/node_stats/?node_data=' + node_data)
    .then(function (data) {
      if (d3.select('.stat-box').empty()) {

        is_affordable = null;

        if(data['is_affordable'] != null) {
            if(data['is_affordable']) {
                is_affordable = 'Yes'
            } else {
                is_affordable = 'No'
            }
        }
          stats = []
          if(data['violent_crime'] != null) {
            stats.push('Violent Crime: ' + data['violent_crime'])
          }
          if(data['property_crime'] != null) {
            stats.push('Property Crime: ' + data['property_crime'])
          }

          if(data['num_of_schools'] != 0) {
            stats.push('Best Schools Count: ' + data['num_of_schools'])
          }

          if(data['avg_avg_annual_income'] != null) {
            stats.push('Avg Annual Income: ' + data['avg_avg_annual_income'])
          }

          if(data['avg_median_annual_income'] != null) {
            stats.push('Avg Median Income: ' + data['avg_median_annual_income'])
          }

          if(is_affordable != null) {
            stats.push('Affordable: ' + is_affordable)
          }

        if(stats.length != 0) {
        var statBox = svg.append('g').attr('class', 'stat-box');

        statBox
          .append("rect")
          .attr("class", "stat-box")
          .attr("height", "150px")
          .attr("width", "250px")
          .attr("x", x)
          .attr("y", y)
          .attr("fill", "rgb(81, 116 ,187)")
          .attr("stroke", "rgb(57, 83, 137)")
          .attr("stroke-width", 2)

        statBox
          .selectAll(".stat-line")
          .data(stats)
          .enter()
          .append("text")
          .attr("class", "stat-line")
          .attr("y", function(_, i) {
            return y + 22 + 20 * i;
          })
          .attr("x", x + 12)
          .attr("font-size", "15px")
          .attr("fill", "white")
          .attr("text-anchor", "start")
          .text(function(d) {
            return d;
          })
        }

      }
    });
}

// Node drag start function
function nodeOnDragStart(d) {
  removeRightClickMenu();
  removeStatBox();
  d3.select(this).classed('active', true);
}

function displayStats(node_type, node_id, className) {
  node_data = node_type + '_' + node_id
  d3.json('/api/node_stats/?node_data=' + node_data)
    .then(function (data) {
      if (d3.select('.stat-box').empty()) {
        var statBox = svg.append('g').attr('class', 'stat-box');

        var node = d3.select(className);
        var x = parseInt(node.attr('cx')) + 10;
        var y = parseInt(node.attr('cy')) + 10;

        statBox.append('rect')
          .attr('class', 'stat-box')
          .attr('height', '150px')
          .attr('width', '250px')
          .attr('x', x)
          .attr('y', y)
          .attr('fill', 'rgb(81, 116 ,187)')
          .attr('stroke', 'rgb(57, 83, 137)')
          .attr('stroke-width', 2)

        is_affordable = data['is_affordable'] == true ? 'Yes' : 'No',
          stats = [
            'Violent Crime: ' + data['violent_crime'],
            'Property Crime: ' + data['property_crime'],
            'Best Schools Count: ' + data['num_of_schools'],
            'Avg Annual Income: ' + data['avg_avg_annual_income'],
            'Avg Median Income: ' + data['avg_median_annual_income'],
            'Affordable: ' + is_affordable,
            'Median Price Prediction: ' + 80000
          ];

        statBox.selectAll('.stat-line')
          .data(stats)
          .enter().append('text')
          .attr('class', 'stat-line')
          .attr('y', function (_, i) { return y + 22 + 20 * i })
          .attr('x', x + 12)
          .attr('font-size', '15px')
          .attr('fill', 'white')
          .attr('text-anchor', 'start')
          .text(function (d) { return d });
      }
    });
}

// Create right click menu for state node
function createRightClickMenu(stateName, node) {
  removeRightClickMenu(); // Closes menu if one is currently active

  var rightClickMenu = svg.append('g')
    .attr('class', 'right-click-menu')

  // Remove 'Drag Similar States' option if > 1 state already exists
  options = totalNodes > 1 ? menuOptions.slice(1) : menuOptions;
  functions = totalNodes > 1 ? menuFunctions.slice(1) : menuFunctions;

  var x = parseInt(node.attr('cx'));
  var y = parseInt(node.attr('cy'));

  rightClickMenu
    .selectAll(".right-click-menu-item")
    .data(options)
    .enter()
    .append("rect")
    .attr("class", "right-click-menu-item")
    .attr("height", rightClickMenuItemHeight)
    .attr("width", 225)
    .attr("y", function(_, i) {
      return y + i * 40;
    })
    .attr("x", x)
    .attr("fill", "rgb(81, 116 ,187)")
    .attr("stroke", "rgb(57, 83, 137)")
    .attr("stroke-width", 2)
    .on("click", function(_, i) {
      return functions[i](stateName);
    });


  rightClickMenu
    .selectAll(".right-click-menu-item-label")
    .data(options)
    .enter()
    .append("text")
    .attr("class", "right-click-menu-item-label")
    .attr("y", function(d, i) {
      return y + i * 40 + 25;
    })
    .attr("x", x + 10)
    .attr("font-size", "15px")
    .attr("fill", "white")
    .attr("text-anchor", "start")
    .text(function(d) {
      return d;
    })
    .on("click", function (_, i) {
      return functions[i](stateName);
    })
}

// Remove right click menu if user clicks away
d3.select('.graphical-exploration').on('click', function () {
  var rightClickMenu = d3.selectAll('.right-click-menu')

  if (!rightClickMenu.empty() && d3.event.target.parentNode.className.baseVal !== 'right-click-menu') {
    removeRightClickMenu();
  }
});

// Remove stat box if user moves mouse outside of node/box
d3.select('.graphical-exploration').on('mouseover', function () {
  var statBox = d3.select('.stat-box');
  var target = d3.event.target;

  // This might need refinement
  if (!statBox.empty() && (target.nodeName !== 'circle')) {
    removeStatBox();
  }
});

// Remove right click menu
function removeRightClickMenu() {
  d3.select('.right-click-menu').remove();
}

// Remove stat box
function removeStatBox() {
  d3.select('.stat-box').remove();
}

// Delete all nodes, labels, and lines
function deleteAllNodes() {
  d3.selectAll('.menu-item')
    .attr('fill', 'rgb(81, 116 ,187)');

  // Remove nodes and links associated with deleted state
  graph.links = [];
  graph.nodes = [];

  var node = nodes.selectAll('.node').data(graph.nodes);
  node.exit().remove();

  var link = links.selectAll('.link').data(graph.links);
  link.exit().remove();
  simulation.restart();

  createdNodes = {};
  countyNodes = {
    best: {},
    zip: {},
    safe: {},
    affordable: {}
  };
  nodeGroups = [0, 1, 2];
  totalNodes = 0;

  d3.select('.clear-all').classed('hidden', true);
  d3.select('.clear-all-label').classed('hidden', true);
}

// Makes string lowercase and replaces spaces with dashes for use as classname
function genClassName(str) {
  return str.trim().replace(/\s+/g, '-').toLowerCase();
}

function createLegend(legend) {
  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 10)
    .attr('y', 5)
    .attr('fill', nodeColors[0][0])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 30)
    .attr('y', 5)
    .attr('fill', nodeColors[1][0])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 50)
    .attr('y', 5)
    .attr('fill', nodeColors[2][0])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('text')
    .attr('x', 80)
    .attr('y', 20)
    .text('Best Counties')

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 10)
    .attr('y', 25)
    .attr('fill', nodeColors[0][1])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 30)
    .attr('y', 25)
    .attr('fill', nodeColors[1][1])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 50)
    .attr('y', 25)
    .attr('fill', nodeColors[2][1])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('text')
    .attr('x', 80)
    .attr('y', 40)
    .text('Best ZIP Codes')

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 10)
    .attr('y', 45)
    .attr('fill', nodeColors[0][3])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 30)
    .attr('y', 45)
    .attr('fill', nodeColors[1][3])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 50)
    .attr('y', 45)
    .attr('fill', nodeColors[2][3])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('text')
    .attr('x', 80)
    .attr('y', 60)
    .text('Safe Counties')

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 10)
    .attr('y', 65)
    .attr('fill', nodeColors[0][4])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 30)
    .attr('y', 65)
    .attr('fill', nodeColors[1][4])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('rect')
    .attr('height', 20)
    .attr('width', 20)
    .attr('x', 50)
    .attr('y', 65)
    .attr('fill', nodeColors[2][4])
    .attr('stroke', 'black')
    .attr('stroke-width', 2)

  legend.append('text')
    .attr('x', 80)
    .attr('y', 80)
    .text('Affordable Counties')
}
