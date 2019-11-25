var usStates = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'];
var createdNodes = {};
var totalNodes = 0;
var nodeColors = ['rgb(84, 172, 94)', 'rgb(243, 193, 79)', 'rgb(103, 59, 153)'];

var menuWidth = 200;
var menuItemHeight = 50;
var menuOffset = 60;

var rightClickMenuItemHeight = 40;

var svg = d3.select('svg');

var width = parseInt(svg.style('width'));
var height = parseInt(svg.style('height'))

var menu = svg.append('g')
  .attr('class', 'menu');

createMenu();

// This is a hacky scroll bar since SVGs do not handle scroll events well
// TODO: Scale this for screen size so that users can access all states
// TODO: Make sure this works properly
svg.append('circle')
  .attr('r', 10)
  .attr('cx', width - 10)
  .attr('cy', 0 + 10)
  .call(d3.drag()
    .on('drag', function() {
      if (d3.event.y > 10 && d3.event.y < height - 10) {
        d3.select(this).attr('cy', d3.event.y)
        d3.select('.menu').attr('transform', 'translate(0, ' + -d3.event.y + ')').attr('y-translation', d3.event.y);
      }
    }))

/**
 * List of main functions and brief description
 *
 * createMenu() => Displays the list of states on the right side and sets up handlers and interactions
 *                 This is the only function that runs on initial page load
 * createStateNode() => Creates a node for a state at the location the user drags to
 *                      Enables right click menu creation on user right click
 * createRightClickMenu() => Displays right click menu for node
 * createCountyNodes() => Creates county nodes and links them to a given state
 */


// Create entire right side state menu including clear all button
function createMenu() {
  // "Clear and Start Over" button
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

  // "Clear and Start Over" label
  menu.append('text')
    .attr('class', 'clear-all-label hidden')
    .attr('y', 30)
    .attr('x', width - 120)
    .attr('font-size', '17px')
    .attr('fill', 'white')
    .attr('text-anchor', 'middle')
    .attr('font-weight', 'bold')
    .text('Clear and Start Over')

  // State name menu items
  menu.selectAll('.menu-item')
    .data(usStates)
    .enter().append('rect')
    .attr('class', function (stateName) { return genClassName(stateName) + '-menu-item' + ' menu-item' })
    .attr('height', 50)
    .attr('width', menuWidth)
    .attr('y', function (d, i) { return i * menuItemHeight + menuOffset })
    .attr('x', width - menuWidth - 20)
    .attr('fill', 'rgb(81, 116 ,187)')
    .attr('stroke', 'rgb(57, 83, 137)')
    .attr('stroke-width', 2)
    .call(d3.drag()
      .on('start', menuOnDragStart)
      .on('drag', menuOnDrag)
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
    .text(function (d) { return d })

  // Menu item drag start function
  function menuOnDragStart(d) {
    removeRightClickMenu();

    if (!createdNodes[d] && totalNodes < 3) {
      d3.select(this).attr('fill', nodeColors[totalNodes]);
    }

    d3.select(this).classed('active', true);
    d3.select('.' + d + '-node');
  }

  function menuOnDrag(d) {
    // console.log('drag: ', d3.event)
  }

  // Menu item drag end function
  function menuOnDragEnd(d) {
    d3.select(this).classed('active', false);
    createStateNode(d);
  }
}

// Create state node with text
function createStateNode(stateName, x, y) {
  // Create node and label for state if one does not already exist
  if (!createdNodes[stateName] && totalNodes < 3) {
    var state = svg.append('g')
      .attr('class', 'state ' + genClassName(stateName));

    var yTranslation = d3.select('.menu').attr('y-translation');

    if (!x) {
      x = d3.event.x;
    }

    if (!y) {
      y = d3.event.y - yTranslation;
    }

    // Create state node
    state.data([stateName]).append('circle')
      .attr('class', 'state-node ' + genClassName(stateName) + '-node')
      .attr('r', '20px')
      .attr('cx', x)
      .attr('cy', y)
      .attr('fill', nodeColors[totalNodes])
      .attr('stroke', 'black')
      .attr('stroke-width', '2')
      .call(d3.drag()
        .on('start', nodeOnDragStart)
        .on('drag', stateNodeOnDrag)
        .on('end', nodeOnDragEnd))
      .on('contextmenu', function() {
        d3.event.preventDefault();

        createRightClickMenu(stateName);
      }).on('mouseover', function() {
        // Prevent stat box display if node is being dragged
        if (!d3.select(this).attr('class').includes('active')) {
          displayStats('.' + genClassName(stateName) + '-node') // TODO: Implement this with actual data
        }
      });

    // Create label for state node
    state.append('text')
      .attr('class', 'state-node-label ' + genClassName(stateName) + '-label')
      .attr('y', y - 30)
      .attr('x', x)
      .attr('font-size', '17px')
      .attr('text-anchor', 'middle')
      .attr('font-weight', 'bold')
      .text(stateName)

    // Count number of active state nodes and ensure user cannot add state more than once
    createdNodes[stateName] = true;
    totalNodes++;

    // Enable clear all button
    d3.select('.clear-all').classed('hidden', false);
    d3.select('.clear-all-label').classed('hidden', false);
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
  'Delete State'
];

// Right click menu functions
var menuFunctions = [
  dragSimilarStates,
  showBestCounties,
  showBestZipCodes,
  showSafeCounties,
  showAffordableCounties,
  showAll,
  deleteState
];

// TODO: Remove this option when more than one state node exists
function dragSimilarStates() {
  if (totalNodes === 1) {
    // Dummy states for testing
    // TODO: Replace this with real data
    var similarStates = ['Washington', 'California'];

    for (var i = 0; i < similarStates.length; i++) {
      createStateNode(similarStates[i], d3.event.x + i * 100, d3.event.y + i * 100);
      d3.select('.' + genClassName(similarStates[i]) + '-menu-item').attr('fill', nodeColors[i + 1]);
    }

    removeRightClickMenu();
  }
}

function showBestCounties(stateName) {
  // Dummy counties for testing
  // TODO: Retrieve appropriate counties and data
  var countyList = ['County A', 'County B', 'County C', 'County D', 'County E']
  createCountyNodes(stateName, countyList);
}

function showBestZipCodes(stateName) {
  // Dummy counties for testing
  // TODO: Retrieve appropriate counties and data
  var countyList = ['County A', 'County B', 'County C', 'County D', 'County E']
  createCountyNodes(stateName, countyList);
}

function showSafeCounties(stateName) {
  // Dummy counties for testing
  // TODO: Retrieve appropriate counties and data
  var countyList = ['County A', 'County B', 'County C', 'County D', 'County E']
  createCountyNodes(stateName, countyList);
}

function showAffordableCounties(stateName) {
  // Dummy counties for testing
  // TODO: Retrieve appropriate counties and data
  var countyList = ['County A', 'County B', 'County C', 'County D', 'County E']
  createCountyNodes(stateName, countyList);
}

function selectAllForAllSimilarStates(stateName) {
  // Dummy counties for testing
  // TODO: Retrieve appropriate counties and data
  var countyList = ['County A', 'County B', 'County C', 'County D', 'County E']
  createCountyNodes(stateName, countyList);
}

// TODO: Implement this to handle more than five counties
function showAll(stateName) {
  // Dummy counties for testing
  // TODO: Retrieve appropriate counties and data
  var countyList = ['County A', 'County B', 'County C', 'County D', 'County E']
  createCountyNodes(stateName, countyList);
}

// Delete the state node and all children nodes
function deleteState(stateName) {
  d3.select('.' + genClassName(stateName) + '-menu-item').attr('fill', 'rgb(81, 116 ,187)');
  d3.select('.' + genClassName(stateName)).remove();
  removeRightClickMenu();

  delete createdNodes[stateName];
  totalNodes--;

  // Remove clear all button if no more state nodes exist
  if (totalNodes === 0) {
    d3.select('.clear-all').classed('hidden', true);
    d3.select('.clear-all-label').classed('hidden', true);
  }
}

function createCountyNodes(stateName, countyList) {
  // Remove existing county nodes, lines, and labels
  d3.select('.' + genClassName(stateName) + '-counties').remove();

  var stateNode = d3.select('.' + genClassName(stateName) + '-node');
  var counties = d3.select('.' + genClassName(stateName)).append('g')
    .attr('class', 'counties ' + genClassName(stateName) + '-counties');

  // Create lines from state node to county nodes
  counties.selectAll('.' + genClassName(stateName) + '-county-line')
    .data(countyList).enter()
    .append('line')
    .attr('class', function (d) { return genClassName(stateName) + '-county-line ' + genClassName(d) + '-county-line' })
    .attr('stroke', 'black')
    .attr('stroke-width', 2)
    .attr('stroke-opacity', 0.3)
    .attr('x1', stateNode.attr('cx'))
    .attr('y1', parseInt(stateNode.attr('cy')))
    .attr('x2', function (_, i) { return parseInt(stateNode.attr('cx')) - 100 + i * 50 })
    .attr('y2', function () { return parseInt(stateNode.attr('cy')) + 100 })

  // Regenerate state node
  // This ensure that the line appears beneath it
  var state = d3.select('.' + genClassName(stateName));
  var stateNode = d3.select('.' + genClassName(stateName) + '-node');
  var cx = stateNode.attr('cx');
  var cy = stateNode.attr('cy');
  var fill = stateNode.attr('fill');
  stateNode.remove();

  state.data([stateName]).append('circle')
    .attr('class', 'state-node ' + genClassName(stateName) + '-node')
    .attr('r', '20px')
    .attr('cx', cx)
    .attr('cy', cy)
    .attr('fill', fill)
    .attr('stroke', 'black')
    .attr('stroke-width', '2')
    .call(d3.drag()
      .on('start', nodeOnDragStart)
      .on('drag', stateNodeOnDrag)
      .on('end', nodeOnDragEnd))
    .on('contextmenu', function () {
      d3.event.preventDefault();

      createRightClickMenu(stateName);
    }).on('mouseover', function () {
      // Prevent stat box display if node is being dragged
      if (!d3.select(this).attr('class').includes('active')) {
        displayStats('.' + genClassName(stateName) + '-node') // TODO: Implement this with actual data
      }
    });

  // Create county nodes
  counties.selectAll('.' + genClassName(stateName) + '-county-node')
    .data(countyList).enter()
    .append('circle')
    .attr('class', function (d) { return 'county-node ' + genClassName(stateName) + '-county-node ' + genClassName(d) + '-county-node' })
    .attr('r', '15px')
    .attr('cx', function (_, i) { return parseInt(stateNode.attr('cx')) - 100 + i * 50 })
    .attr('cy', parseInt(stateNode.attr('cy')) + 100)
    .attr('fill', stateNode.attr('fill'))
    .attr('stroke', 'black')
    .attr('stroke-width', 2)
    .attr('state', genClassName(stateName))
    .call(d3.drag()
      .on('start', nodeOnDragStart)
      .on('drag', countyNodeOnDrag)
      .on('end', nodeOnDragEnd))
    .on('mouseover', function (d) {
      // Prevent stat box display if node is being dragged
      if (!d3.select(this).attr('class').includes('active')) {
        displayStats('.' + genClassName(stateName) + '-county-node.' + genClassName(d) + '-county-node') // TODO: Implement this with actual data
      }
    });

  // Create county node labels
  counties.selectAll('.' + genClassName(stateName) + '-county-label')
    .data(countyList).enter()
    .append('text')
    .attr('class', function (d) { return genClassName(stateName) + '-county-label ' + genClassName(d) + '-county-label' })
    .attr('x', function (_, i) { return parseInt(stateNode.attr('cx')) - 100 + i * 50 })
    .attr('y', parseInt(stateNode.attr('cy')) + 70)
    .attr('font-size', '15px')
    .attr('text-anchor', 'middle')
    .attr('font-weight', 'bold')
    .text(function (d) { return d });

  // Remove the right click menu if everything is successful
  removeRightClickMenu();
}

// Node drag start function
function nodeOnDragStart(d) {
  removeRightClickMenu();
  removeStatBox();
  d3.select(this).classed('active', true);
}

// Drag function for state nodes, lines, and labels
function stateNodeOnDrag(stateName) {
  var stateLineClass = '.' + genClassName(stateName) + '-county-line';
  d3.selectAll(stateLineClass)
    .attr('x1', d3.event.x)
    .attr('y1', d3.event.y)

  d3.select(this)
    .attr('cx', d3.event.x)
    .attr('cy', d3.event.y)

  var stateLabelClass = '.' + genClassName(stateName) + '-label';
  d3.select(stateLabelClass)
    .attr('x', d3.event.x)
    .attr('y', d3.event.y - 30)
}

// Drag function for county nodes, lines, and labels
function countyNodeOnDrag(countyName) {
  var stateName = d3.select(this).attr('state');

  var countyLineClass = '.' + stateName + '-county-line' + '.' + genClassName(countyName) + '-county-line';
  d3.select(countyLineClass)
    .attr('x2', d3.event.x)
    .attr('y2', d3.event.y)

  d3.select(this)
    .attr('cx', d3.event.x)
    .attr('cy', d3.event.y)

  var countyLabelClass = '.' + stateName + '-county-label' + '.' + genClassName(countyName) + '-county-label';
  d3.select(countyLabelClass)
    .attr('x', d3.event.x)
    .attr('y', d3.event.y - 30)
}

// Node drag end function
function nodeOnDragEnd(d) {
  d3.select(this).classed('active', false);
}

function displayStats(className) {
  if (d3.select('.stat-box').empty()) {
    var statBox = svg.append('g').attr('class', 'stat-box');

    var node = d3.select(className);
    var x = parseInt(node.attr('cx')) + 10;
    var y = parseInt(node.attr('cy')) + 10;

    statBox.append('rect')
      .attr('class', 'stat-box')
      .attr('height', '95px')
      .attr('width', '250px')
      .attr('x', x)
      .attr('y', y)
      .attr('fill', 'rgb(81, 116 ,187)')
      .attr('stroke', 'rgb(57, 83, 137)')
      .attr('stroke-width', 2)

    // TODO: Get actual stats
    stats = [
      'Crime Rate: ' + 20.5,
      'Best Schools Count: ' + 10,
      'Median Price Prediction: ' + 80000,
      'Affordable: ' + 'Yes'
    ];

    statBox.selectAll('.stat-line')
      .data(stats)
      .enter().append('text')
      .attr('class', 'stat-line')
      .attr('y', function(_, i) { return y + 22 + 20 * i })
      .attr('x', x + 12)
      .attr('font-size', '15px')
      .attr('fill', 'white')
      .attr('text-anchor', 'start')
      .text(function (d) { return d });
  }
}

// Create right click menu for state node
function createRightClickMenu(stateName) {
  removeRightClickMenu(); // Closes menu if one is currently active

  var rightClickMenu = svg.append('g')
    .attr('class', 'right-click-menu')

  // Remove "Drag Similar States" option if > 1 state already exists
  options = totalNodes > 1 ? menuOptions.slice(1) : menuOptions;
  functions = totalNodes > 1 ? menuFunctions.slice(1) : menuFunctions;

  rightClickMenu.selectAll('.right-click-menu-item')
    .data(options)
    .enter().append('rect')
    .attr('class', 'right-click-menu-item')
    .attr('height', rightClickMenuItemHeight)
    .attr('width', 210)
    .attr('y', function (_, i) { return d3.event.y + i * 40 })
    .attr('x', d3.event.x)
    .attr('fill', 'rgb(81, 116 ,187)')
    .attr('stroke', 'rgb(57, 83, 137)')
    .attr('stroke-width', 2)
    .on('click', function (_, i) { return functions[i](stateName) })

  rightClickMenu.selectAll('.right-click-menu-item-label')
    .data(options)
    .enter().append('text')
    .attr('class', 'right-click-menu-item-label')
    .attr('y', function (d, i) { return d3.event.y + i * 40 + 25 })
    .attr('x', d3.event.x + 10)
    .attr('font-size', '15px')
    .attr('fill', 'white')
    .attr('text-anchor', 'start')
    .text(function (d) { return d })
}

// Remove right click menu if user clicks away
d3.select('.graphical-exploration').on('click', function() {
  var rightClickMenu = d3.selectAll('.right-click-menu')

  if (!rightClickMenu.empty() && d3.event.target.parentNode.className.baseVal !== 'right-click-menu') {
    removeRightClickMenu();
  }
});

// Remove stat box if user moves mouse outside of node/box
d3.select('.graphical-exploration').on('mouseover', function() {
  var statBox = d3.select('.stat-box');
  var className = d3.event.target.className.baseVal;

  if (!statBox.empty() && (!className.includes('stat-box') && !className.includes('state-node') && !className.includes('county-node') && !className.includes('stat-line'))) {
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
  d3.selectAll('.state').remove();

  d3.selectAll('.menu-item')
    .attr('fill', 'rgb(81, 116 ,187)');

  createdNodes = {};
  totalNodes = 0;

  d3.select('.clear-all').classed('hidden', true);
  d3.select('.clear-all-label').classed('hidden', true);
}

// Makes string lowercase and replaces spaces with dashes for use as classname
function genClassName(str) {
  return str.replace(/\s+/g, '-').toLowerCase();
}
