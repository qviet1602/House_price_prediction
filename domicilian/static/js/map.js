var svg = d3.select('svg');

// TODO: Make map responsive
var width = parseInt(svg.style('width'));
var height = parseInt(svg.style('height'));

var rentalPrices = d3.map();
var purchasePrices = d3.map();
var projection = d3.geoAlbersUsa().translate([width/2, 250]).scale([1000])
var path = d3.geoPath().projection(projection);

var promises = [
  d3.json('/static/json/states-10m.json'),
  d3.json('/api/rental_median_prices/'),
  d3.json('/api/purchase_median_prices/')
];

Promise.all(promises).then(ready);

function ready([us, rental, purchase]) {
   for(var i=0; i<rental.length;i++) {
	key = rental[i]['name']
        hash_value = {}
        hash_value['RegionName'] = rental[i]['name']
        hash_value['RegionID'] = rental[i]['state_code']
        hash_value['2019-09'] = rental[i]['list_price']
        rentalPrices.set(key, hash_value);
   }
   for(var i=0; i<purchase.length;i++) {
	key = purchase[i]['name']
        hash_value = {}
        hash_value['RegionName'] = purchase[i]['name']
        hash_value['RegionID'] = purchase[i]['state_code']
        hash_value['2019-09'] = purchase[i]['list_price']
        purchasePrices.set(key, hash_value);
   }
  // Default to rental prices
  updateMap(us, rentalPrices, d3.schemeBlues[9], 'Zillow Rent Index (ZRI)');

  d3.select('#select')
    .on('change', function() {
      svg.select('.states').remove();
      var type = document.querySelector('input[name="type"]:checked').value

      if (type === 'rentals') {
        updateMap(us, rentalPrices, d3.schemeBlues[9], 'Zillow Rent Index (ZRI)');
      } else if (type === 'purchases') {
        updateMap(us, purchasePrices, d3.schemeReds[9], 'Zillow Home Value Index (ZHVI)');
      }
    });
}

function updateMap(us, prices, colorScheme, index) {
  var min = d3.min(prices.values(), function(d) { return d['2019-09'] });
  var max = d3.max(prices.values(), function(d) { return d['2019-09'] });

  var x = d3.scaleLinear()
    .domain([min, max])
    .range([600, 860]);

  var schemeSteps = 9;
  var colorStep = (max - min) / schemeSteps;
  var color = d3.scaleThreshold()
    .domain(d3.range(min + colorStep, max, colorStep))
    .range(colorScheme);

  svg.append('g')
    .attr('class', 'states')
    .selectAll('path')
    .data(topojson.feature(us, us.objects.states).features)
    .enter().append('path')
    .attr('fill', function(d) {
      var price = prices.get(d.properties.name);
      if (price) {
        return color(price['2019-09']);
      } else {
        return color(min);
      }
    })
    .attr('stroke', 'black')
    .attr('stroke-width', 1)
    .attr('d', path)
    .on('click', function(d) {
      var state = prices.get(d.properties.name)['RegionID'];
      document.cookie = 'state=' + state;

      // TODO: Click should take user to state county screen
    })
    .on('mouseover', function() {
      d3.select(this).attr('stroke-width', 3)
    })
    .on('mouseout', function () {
      d3.select(this).attr('stroke-width', 1)
    });


  // TODO: Update the legend without removing it each time
  svg.select('.key').remove();
  updateLegend(color, x, index);
}

function updateLegend(color, x, index) {
  var g = svg.append('g')
    .attr('class', 'key')
    .attr('transform', 'translate(450, 400)')

  g.selectAll('rect')
    .data(color.range().map(function(d) {
      d = color.invertExtent(d);
      if (d[0] == null) d[0] = x.domain()[0];
      if (d[1] == null) d[1] = x.domain()[1];
      return d;
    }))
    .enter().append('rect')
      .attr('height', 8)
      .attr('x', function(d) { return x(d[0]); })
      .attr('width', function(d) { return x(d[1]) - x(d[0]); })
      .attr('fill', function(d) { return color(d[0]); });

  g.append('text')
    .attr('class', 'caption')
    .attr('x', x.range()[0])
    .attr('y', -6)
    .attr('fill', '#000')
    .attr('text-anchor', 'start')
    .attr('font-weight', 'bold')
    .text(index);

  g.call(d3.axisBottom(x)
    .tickSize(13)
    .tickFormat(function (x, i) { return Math.round(x) })
    .tickValues(color.domain()))
    .select('.domain')
    .remove().exit()

  g.selectAll('.tick text')
    .attr('text-anchor', 'end')
    .attr('transform', 'rotate(-30)')
}
