// Define custom icons
function schoolIcon (feature, latlng) {
  var redMarker = L.AwesomeMarkers.icon({
    icon: 'graduation-cap',
    markerColor: 'purple',
    prefix: 'fa',
    extraClasses: 'schools-icon',
  });
  return L.marker(latlng, { icon: redMarker })
}

function forRentIcon (feature, latlng) {
  var rentMarker = L.AwesomeMarkers.icon({
    icon: 'home',
    markerColor: 'lightred',
    prefix: 'fa',
    extraClasses: 'forrent-icon',
  });
  return L.marker(latlng, { icon: rentMarker })
}

function forSaleIcon (feature, latlng) {
  var saleMarker = L.AwesomeMarkers.icon({
    icon: 'home',
    markerColor: 'lightgreen',
    prefix: 'fa',
    extraClasses: 'forsale-icon',
  });
  return L.marker(latlng, { icon: saleMarker })
}

function bizIcon (feature, latlng) {
  var bizMarker = L.AwesomeMarkers.icon({
    icon: 'shopping-cart',
    markerColor: 'lightblue',
    prefix: 'fa',
    extraClasses: 'biz-icon',
  });
  return L.marker(latlng, { icon: bizMarker })
}

// Function to toggle marker layers
function toggleSchools() {
  if(!toggle) {
    map.removeLayer(schoolsLayer);
    var schools = d3.select('#schoolsToggle')
      .style('background-color', 'white');
      var schoolsInfo = d3.select("#schoolsInfo")
      .style('color', 'black');
  } else {
    map.addLayer(schoolsLayer);
    var schools = d3.select('#schoolsToggle')
      .style('background-color', 'DodgerBlue');
    var schoolsInfo = d3.select("#schoolsInfo")
      .style('color', 'white');
  }
  toggle = !toggle;
};

function toggleForSale() {
  if(!toggle) {
    map.removeLayer(salesLayer);
    var salestoggles = d3.select('#forSaleToggle')
      .style('background-color', 'white');
      var salesInfo = d3.select("#salesInfo")
      .style('color', 'black');
  } else {
    map.addLayer(salesLayer);
    var salestoggles = d3.select('#forSaleToggle')
      .style('background-color', 'DodgerBlue');
    var salesInfo = d3.select("#salesInfo")
      .style('color', 'white');
  }
  toggle = !toggle;
};

function toggleForRent() {
  if(!toggle) {
    map.removeLayer(rentalsLayer);
    var rentals = d3.select('#rentalsToggle')
      .style('background-color', 'white');
      var rentalsInfo = d3.select("#rentalsInfo")
      .style('color', 'black');
  } else {
    map.addLayer(rentalsLayer);
    var rentals = d3.select('#rentalsToggle')
      .style('background-color', 'DodgerBlue');
    var rentalsInfo = d3.select("#rentalsInfo")
      .style('color', 'white');
  }
  toggle = !toggle;
};

function toggleBiz() {
  if(!toggle) {
    map.removeLayer(bizLayer);
    var schools = d3.select('#bizToggle')
      .style('background-color', 'white');
      var schoolsInfo = d3.select("#bizInfo")
      .style('color', 'black');
  } else {
    map.addLayer(bizLayer);
    var schools = d3.select('#bizToggle')
      .style('background-color', 'DodgerBlue');
    var schoolsInfo = d3.select("#bizInfo")
      .style('color', 'white');
  }
  toggle = !toggle;
};

//Get schools data
async function getSchools(lat,long) {

  return new Promise(function (resolve, reject) {
    var apikey = 'bbe0840065msh8c5d63ec1c6386ep1dcdfdjsnebfa3333d0f5';
    var api_url = 'realtor.p.rapidapi.com';

    var request_url = 'https://' 
      + api_url
      + '/schools/list-nearby?'
      + 'lon=' + encodeURIComponent(long)
      + '&lat=' + encodeURIComponent(lat)

    var request1 = new XMLHttpRequest();
    request1.open('GET', request_url, true);
    request1.setRequestHeader("x-rapidapi-host", api_url)
    request1.setRequestHeader("x-rapidapi-key", apikey)
    
    request1.onload = function() {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request1.status == 200){ 
        // Success!
        var data = JSON.parse(request1.responseText);
        resolve(data['schools'])

      } else if (request1.status <= 500){ 
        // We reached our target server, but it returned an error
                            
        console.log("unable to geocode! Response code: " + request1.status);
        var data = JSON.parse(request1.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request1.onerror = function() {
      // There was a connection error of some sort
      console.log("unable to connect to server");        
    };

    request1.send();  // make the request
  });
};



// plot schools data
function plotSchools(schools) { 

  
  data = []
  
  schools.forEach(d => {
    var education_levels = [];
    d.education_levels.forEach(e => {
      var capped =  e.charAt(0).toUpperCase() + e.slice(1);
      education_levels.push(capped)
    });
    schoolJson =
    {
      id: d.id,
      type: "Feature",
      properties: {
        "Name": d.name,
        "Level(s)": education_levels.toString(),
        "Type": d.funding_type.charAt(0).toUpperCase() + d.funding_type.slice(1),
        "Great Schools Rating": d.ratings['great_schools_rating'] || 'None' ,
        "Address": d.location.street + ' ' + d.location.city + ', ' + d.location.state + ' ' + d.location.postal_code,
        "Phone": d.phone,
        "Student-Teacher Ratio": d.student_teacher_ratio || 'None',
        "District": d.district.name || 'None'
    },
      geometry: {
        coordinates: [d.lon, d.lat],
        type: "Point"
      }
    };
    data.push(schoolJson);
  })

  //callback for onEachFeature
  function onSchools(feature, layer) {
  schoolsLayer.addLayer(layer);
  window.toggle = false;
  layer.on('mouseover', function () {
      layer.bindPopup('<b>' + 'Name:</b> ' + feature.properties.Name + '</br><br>'
                        + '<b>Level(s):</b> ' + feature.properties['Level(s)'] + '<br><br>'
                        + '<b>Type:</b> ' + feature.properties.Type + '<br><br>'
                        + '<b>Great Schools Rating:</b> ' + feature.properties['Great Schools Rating']).openPopup();
    });
    layer.on('mouseout', function () {
      layer.closePopup();
    });
    layer.on('click', function () {
      // Let's say you've got a property called url in your geojsonfeature:
      var details = d3.select('#details')
      details.selectAll("text").remove();
      details.selectAll("tspan").remove();

      sidebar.open('details');
      details.append('text')
        .attr("y", 20)
        .attr('class','details-h2')
        .text('School Details')
        .append('br')

        Object.keys(feature.properties).forEach(function (item) {
          details.append('tspan')
            .text(item + ': ')
            .attr('class', 'key')
           
           
          details.append('tspan')
            .text(feature.properties[item])
            .attr('class', 'value')
            .attr("dy", 25)
            .append('br');
      });
    });
  };

  L.geoJSON(data, {
    pointToLayer: schoolIcon,
    onEachFeature: onSchools
}).addTo(map);
};

//get rental listings
async function getForRent(postal) {

return new Promise(function (resolve, reject) {
  var apikey = 'bbe0840065msh8c5d63ec1c6386ep1dcdfdjsnebfa3333d0f5';
  var api_url = 'realtor.p.rapidapi.com';

  var request_url = 'https://' 
    + api_url
    + '/properties/list-for-rent?'
    + 'radius=5'
    + '&sort=relevance'
    + '&limit=50'
    + '&postal_code=' + encodeURIComponent(postal)

  var request2 = new XMLHttpRequest();
  request2.open('GET', request_url, true);
  request2.setRequestHeader("x-rapidapi-host", api_url)
  request2.setRequestHeader("x-rapidapi-key", apikey)
  
  request2.onload = function() {
    // see full list of possible response codes:
    // https://opencagedata.com/api#codes

    if (request2.status == 200){ 
      // Success!
      var data = JSON.parse(request2.responseText);
      // console.log(data['schools']);
      resolve(data.listings)

    } else if (request2.status <= 500){ 
      // We reached our target server, but it returned an error
                          
      console.log("unable to geocode! Response code: " + request2.status);
      var data = JSON.parse(request2.responseText);
      console.log(data.status.message);
    } else {
      console.log("server error");
    }
  };
  request2.onerror = function() {
    // There was a connection error of some sort
    console.log("unable to connect to server");        
  };

  request2.send();  // make the request
});
};

// get sale listings
async function getForSale(postal) {

  return new Promise(function (resolve, reject) {
    var apikey = 'bbe0840065msh8c5d63ec1c6386ep1dcdfdjsnebfa3333d0f5';
    var api_url = 'realtor.p.rapidapi.com';
  
    var request_url = 'https://' 
      + api_url
      + '/properties/list-for-sale?'
      + 'radius=5'
      + '&sort=relevance'
      + '&limit=50'
      + '&postal_code=' + encodeURIComponent(postal)
  
    var request2 = new XMLHttpRequest();
    request2.open('GET', request_url, true);
    request2.setRequestHeader("x-rapidapi-host", api_url)
    request2.setRequestHeader("x-rapidapi-key", apikey)
    
    request2.onload = function() {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes
  
      if (request2.status == 200){ 
        // Success!
        var data = JSON.parse(request2.responseText);
        // console.log(data['schools']);
        resolve(data.listings)
  
      } else if (request2.status <= 500){ 
        // We reached our target server, but it returned an error
                            
        console.log("unable to geocode! Response code: " + request2.status);
        var data = JSON.parse(request2.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request2.onerror = function() {
      // There was a connection error of some sort
      console.log("unable to connect to server");        
    };
  
    request2.send();  // make the request
  });
  };

// reverse geocode address

async function getAddress(lat,long) {
  return new Promise(function (resolve, reject) {
  var apikey = 'a68a77d7a9344a27b1eb9bc2821719c5';
  var api_url = 'https://api.opencagedata.com/geocode/v1/json';

  var request_url = api_url
    + '?'
    + 'key=' + apikey
    + '&q=' + encodeURIComponent(lat + ',' + long);
    // + '&pretty=1'
    // + '&no_annotations=1';

  var request = new XMLHttpRequest();
  request.open('GET', request_url, true);

  request.onload = function() {
    // see full list of possible response codes:
    // https://opencagedata.com/api#codes

    if (request.status == 200){ 
      // Success!
      var data = JSON.parse(request.responseText);
      resolve(data.results[0].components.postcode);

    } else if (request.status <= 500){ 
      // We reached our target server, but it returned an error
                           
      console.log("unable to geocode! Response code: " + request.status);
      var data = JSON.parse(request.responseText);
      console.log(data.status.message);
    } else {
      console.log("server error");
    }
  };
  request.onerror = function() {
    // There was a connection error of some sort
    console.log("unable to connect to server");        
  };

  request.send();  // make the request
  });
  };

  //get buisness data
  async function getbiz1(lat,lon) {

    return new Promise(function (resolve, reject) {
      var apikey = 'zhWUU_2WcNraf8boB_mVxaa1yc-818kp9wl511sWCCAqRp83v-XTli6yH9d_UQnVK0u3gYgkgB3QGidj7_jGdHniL1nzSgRzyfDK0-kwvf81LUPg1gW8wr12p0jbXXYx';
      var api_url = 'https://cold-fire-e963.jflick-cors.workers.dev/?https://api.yelp.com/v3/businesses/search';
    
      var request_url = api_url
        + '?'
        + '&limit=50'
        + '&radius=565'
        + '&sort_by=distance'
        + '&latitude=' + encodeURIComponent(lat)
        + '&longitude=' + encodeURIComponent(lon)
    
      var request3 = new XMLHttpRequest();
      request3.open('GET', request_url, true);
      request3.setRequestHeader("Authorization", 'Bearer ' + apikey)
      // request3.withCredentials = "true";
      
      request3.onload = function() {
        // see full list of possible response codes:
        // https://opencagedata.com/api#codes
    
        if (request3.status == 200){ 
          // Success!
          var data = JSON.parse(request3.responseText);
          // console.log(data['schools']);
          console.log(data);
          resolve(data.businesses)
    
        } else if (request3.status <= 500){ 
          // We reached our target server, but it returned an error
          console.log(request3.responseText)                 
          console.log("unable to geocode! Response code: " + request3.status);
          var data = JSON.parse(request3.responseText);
          console.log(data.status.message);
        } else {
          console.log("server error");
        }
      };
      request3.onerror = function() {
        // There was a connection error of some sort
        console.log("unable to connect to server");        
      };
    
      request3.send();  // make the request
    });
    };

    //get buisness data
  async function getbiz2 (lat,lon) {

    return new Promise(function (resolve, reject) {
      var apikey = 'zhWUU_2WcNraf8boB_mVxaa1yc-818kp9wl511sWCCAqRp83v-XTli6yH9d_UQnVK0u3gYgkgB3QGidj7_jGdHniL1nzSgRzyfDK0-kwvf81LUPg1gW8wr12p0jbXXYx';
      var api_url = 'https://cold-fire-e963.jflick-cors.workers.dev/?https://api.yelp.com/v3/businesses/search';
    
      var request_url = api_url
        + '?'
        + '&limit=50'
        + '&radius=565'
        + '&offset=50'
        + '&sort_by=distance'
        + '&latitude=' + encodeURIComponent(lat)
        + '&longitude=' + encodeURIComponent(lon)
    
      var request3 = new XMLHttpRequest();
      request3.open('GET', request_url, true);
      request3.setRequestHeader("Authorization", 'Bearer ' + apikey)
      // request3.withCredentials = "true";
      
      request3.onload = function() {
        // see full list of possible response codes:
        // https://opencagedata.com/api#codes
    
        if (request3.status == 200){ 
          // Success!
          var data = JSON.parse(request3.responseText);
          // console.log(data['schools']);
          console.log(data);
          resolve(data.businesses)
    
        } else if (request3.status <= 500){ 
          // We reached our target server, but it returned an error
          console.log(request3.responseText)                 
          console.log("unable to geocode! Response code: " + request3.status);
          var data = JSON.parse(request3.responseText);
          console.log(data.status.message);
        } else {
          console.log("server error");
        }
      };
      request3.onerror = function() {
        // There was a connection error of some sort
        console.log("unable to connect to server");        
      };
    
      request3.send();  // make the request
    });
    };

  //get buisness data
  async function getbiz3 (lat,lon) {

    return new Promise(function (resolve, reject) {
      var apikey = 'zhWUU_2WcNraf8boB_mVxaa1yc-818kp9wl511sWCCAqRp83v-XTli6yH9d_UQnVK0u3gYgkgB3QGidj7_jGdHniL1nzSgRzyfDK0-kwvf81LUPg1gW8wr12p0jbXXYx';
      var api_url = 'https://cold-fire-e963.jflick-cors.workers.dev/?https://api.yelp.com/v3/businesses/search';
    
      var request_url = api_url
        + '?'
        + '&limit=50'
        + '&radius=565'
        + '&offset=100'
        + '&sort_by=distance'
        + '&latitude=' + encodeURIComponent(lat)
        + '&longitude=' + encodeURIComponent(lon)
    
      var request3 = new XMLHttpRequest();
      request3.open('GET', request_url, true);
      request3.setRequestHeader("Authorization", 'Bearer ' + apikey)
      // request3.withCredentials = "true";
      
      request3.onload = function() {
        // see full list of possible response codes:
        // https://opencagedata.com/api#codes
    
        if (request3.status == 200){ 
          // Success!
          var data = JSON.parse(request3.responseText);
          // console.log(data['schools']);
          console.log(data);
          resolve(data.businesses)
    
        } else if (request3.status <= 500){ 
          // We reached our target server, but it returned an error
          console.log(request3.responseText)                 
          console.log("unable to geocode! Response code: " + request3.status);
          var data = JSON.parse(request3.responseText);
          console.log(data.status.message);
        } else {
          console.log("server error");
        }
      };
      request3.onerror = function() {
        // There was a connection error of some sort
        console.log("unable to connect to server");        
      };
    
      request3.send();  // make the request
    });
    };

// plot rental data
function plotForRent(rentalListings) { 

data = []

rentalListings.forEach(d => {
  rentalJson =
  {
    id: d.listing_id,
    type: "Feature",
    properties: {
      "Name": d.name,
      "Beds": d.beds,
      "Baths": d.baths,
      "Price": d.price,
      "Pets": d.pet_policy,
      "Square Footage": d.sqft,
      "Address": d.address,
      
  },
    geometry: {
      coordinates: [d.lon, d.lat],
      type: "Point"
    }
  };
  data.push(rentalJson);
})

function onRentals(feature, layer) {
rentalsLayer.addLayer(layer);
window.toggle = false;
layer.on('mouseover', function () {
    layer.bindPopup('<b>' + 'Name:</b> ' + feature.properties.Name + '</br><br>'
                      + '<b>Beds:</b> ' + feature.properties.Beds + '<br><br>'
                      + '<b>Baths:</b> ' + feature.properties.Baths + '<br><br>'
                      + '<b>Price:</b> ' + feature.properties.Price).openPopup();
  });
  layer.on('mouseout', function () {
    layer.closePopup();
  });
  layer.on('click', function () {
    var details = d3.select('#details')
    details.selectAll("text").remove();
    details.selectAll("tspan").remove();

    sidebar.open('details');
    details.append('text')
      .attr("y", 20)
      .attr('class','details-h2')
      .text('Rental Details')
      .append('br')

      Object.keys(feature.properties).forEach(function (item) {
        details.append('tspan')
          .text(item + ': ')
          .attr('class', 'key')
         
         
        details.append('tspan')
          .text(feature.properties[item])
          .attr('class', 'value')
          .attr("dy", 25)
          .append('br');
    });
  });
};

L.geoJSON(data, {
  pointToLayer: forRentIcon,
  onEachFeature: onRentals
}).addTo(map);

};

// plot sales data
function plotForSale(salesListings) { 

  data = []
  
  salesListings.forEach(d => {
    saleJson =
    {
      id: d.listing_id,
      type: "Feature",
      properties: {
        "Name": d.address,
        "Beds": d.beds,
        "Baths": d.baths,
        "Price": d.price,
        "Square Footage": d.sqft,
        "Lot Size": d.lot_size,
        "Address": d.address,
        "Type": d.prop_type,
        "URL": d.rdc_web_url,  
    },
      geometry: {
        coordinates: [d.lon, d.lat],
        type: "Point"
      }
    };
    data.push(saleJson);
  })
  
  function onSales(feature, layer) {
  salesLayer.addLayer(layer);
  window.toggle = false;
  layer.on('mouseover', function () {
      layer.bindPopup('<b>' + 'Name:</b> ' + feature.properties.Name + '</br><br>'
                        + '<b>Beds:</b> ' + feature.properties.Beds + '<br><br>'
                        + '<b>Baths:</b> ' + feature.properties.Baths + '<br><br>'
                        + '<b>Price:</b> ' + feature.properties.Price).openPopup();
    });
    layer.on('mouseout', function () {
      layer.closePopup();
    });
    layer.on('click', function () {
      var details = d3.select('#details')
      details.selectAll("text").remove();
      details.selectAll("tspan").remove();
  
      sidebar.open('details');
      details.append('text')
        .attr("y", 20)
        .attr('class','details-h2')
        .text('Listing Details')
        .append('br')
  
        Object.keys(feature.properties).forEach(function (item) {
          details.append('tspan')
            .text(item + ': ')
            .attr('class', 'key')
           
           
          details.append('tspan')
            .text(feature.properties[item])
            .attr('class', 'value')
            .attr("dy", 25)
            .append('br');
      });
    });
  };
  
  L.geoJSON(data, {
    pointToLayer: forSaleIcon,
    onEachFeature: onSales
  }).addTo(map);
  };

// plot buisness data
function plotBiz(businesses) { 

  data = []
  
  businesses.forEach(d => {
    bizJson =
    {
      id: d.id,
      type: "Feature",
      properties: {
        "Name": d.name,
        "Category": d.categories[0].title || '',
        "Location": d.location.display_address.toString(),
        "Yelp Rating": d.rating,
        "Phone": d.display_phone, 
        "Price": d.price, 
        "Yelp Link": d.url
    },
      geometry: {
        coordinates: [d.coordinates.longitude, d.coordinates.latitude],
        type: "Point"
      }
    };
    data.push(bizJson);
  })
  
  function onBiz(feature, layer) {
  bizLayer.addLayer(layer);
  window.toggle = false;
  layer.on('mouseover', function () {
      layer.bindPopup('<b>' + 'Name:</b> ' + feature.properties.Name + '</br><br>'
                        + '<b>Category:</b> ' + feature.properties.Category + '<br><br>'
                        + '<b>Yelp Rating:</b> ' + feature.properties["Yelp Rating"] + '<br><br>'
                        + '<b>Price:</b> ' + feature.properties.Price).openPopup();
    });
    layer.on('mouseout', function () {
      layer.closePopup();
    });
    layer.on('click', function () {
      var details = d3.select('#details')
      details.selectAll("text").remove();
      details.selectAll("tspan").remove();
  
      sidebar.open('details');
      details.append('text')
        .attr("y", 20)
        .attr('class','details-h2')
        .text('Business Details')
        .append('br')
  
        Object.keys(feature.properties).forEach(function (item) {
          details.append('tspan')
            .text(item + ': ')
            .attr('class', 'key')
           
           
          details.append('tspan')
            .text(feature.properties[item])
            .attr('class', 'value')
            .attr("dy", 25)
            .append('br');
      });
    });
  };
  
  L.geoJSON(data, {
    pointToLayer: bizIcon,
    onEachFeature: onBiz
  }).addTo(map);
  };


// define max bounds of the map (not sure if working correctly)
  var maxBounds =  L.latLngBounds(
  L.latLng(5.499550, -167.276413),
  L.latLng(83.162102, -52.233040)
);

// mapid is the id of the div where the map will appear
var map = L
  .map('mapid')
  .fitBounds(maxBounds)
  // .setView(new L.LatLng(38.54734730982558, -121.7376619577408), 18); //testing purposess
  .setView(new L.LatLng(37.689740802722724, -109.599609375), 5); 
  // .setView([47, 2], 10)
  // .setView([40, -8025], 10);   // center position + zoom

// MAIN FUNCTION
map.on('click', async function(e) {
    // alert("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng) //for debugging
    dropTile(e.latlng.lat, e.latlng.lng);
    var schools = await getSchools(e.latlng.lat, e.latlng.lng);
    plotSchools(schools);
    var postal_code = await getAddress(e.latlng.lat, e.latlng.lng);
    var rentals = await getForRent(postal_code);
    plotForRent(rentals);
    var sales = await getForSale(postal_code);
    plotForSale(sales);

    //I know this is messy but it's 1:30 AM and I had too much caffeine.
    var bizList1 = await getbiz1(e.latlng.lat, e.latlng.lng);
    var bizList2 = await getbiz2(e.latlng.lat, e.latlng.lng);
    var bizList3 = await getbiz3(e.latlng.lat, e.latlng.lng);
    plotBiz(bizList1);
    plotBiz(bizList2);
    plotBiz(bizList3);

  });


//Init Sidebar
var sidebar = L.control.sidebar({ container: 'sidebar' })
            .addTo(map)
            .open('home');
        // add panels dynamically to the sidebar
        sidebar
            .addPanel({
                id:   'Filter Views',
                tab:  '<i class="fa fa-filter"></i>',
                title: 'Filter Views',
                pane: '<p>Drop a pin on the area that you want to check out, then use the options below to filter what you see on the map. <p/>' +
                '<p id="forSaleToggle"><button onclick="toggleForSale()" class="homesForSale"><i class="fa fa-home"></i></button><text id="salesInfo" class="buttonInfo">Homes For Sale</text></p>' +
                '<p id="rentalsToggle"><button onclick="toggleForRent()" class="homesForRent"><i class="fa fa-home"></i></button><text id="rentalsInfo" class="buttonInfo">Homes For Rent</text></p>' +
                '<p id="schoolsToggle"><button onclick="toggleSchools()" class="schools"><i class="fa fa-graduation-cap"></i></button><text id="schoolsInfo" class="buttonInfo">Schools</text></p>' + 
               '<p id="bizToggle"><button onclick="toggleBiz()" class="businesses"><i class="fa fa-shopping-cart"></i></button><text id="bizInfo" class="buttonInfo">Businesses</text></p>',

            })            
        // be notified when a panel is opened
        sidebar.on('content', function (ev) {
            switch (ev.id) {
                case 'details':
                sidebar.options.details = true;
                break;
                default:
                sidebar.options.details = false;
            }
        });
        var userid = 0
        function addUser() {
            sidebar.addPanel({
                id:   'user' + userid++,
                tab:  '<i class="fa fa-user"></i>',
                title: 'User Profile ' + userid,
                pane: '<p>user ipsum dolor sit amet</p>',
            });
        }

// callback to plot a point where the user clicks
function dropTile(lat, long) {
  data = [
    {
      id: "userLoc",
      type: "Feature",
      geometry: {
        coordinates: [long, lat],
        type:"Point"
      }
    }
  ]

var myStyle2 = {
	"color": "#ff7800",
	"weight": 400,
	"opacity": 0.65
};

L.geoJSON(data, {style:myStyle2}
).addTo(map);

};

// Add a tile to the map = a background. Comes from OpenStreetmap
L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>',
    maxZoom: 18,
    }).addTo(map);

//define GeoJSON layer groups. Allows control of groups of markers
var schoolsLayer = L.layerGroup().addTo(map)

var rentalsLayer = L.layerGroup().addTo(map)

var salesLayer = L.layerGroup().addTo(map)

var bizLayer = L.layerGroup().addTo(map)

// Add a svg layer to the map
L.svg().addTo(map);
