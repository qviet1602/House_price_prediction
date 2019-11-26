// Define custom icons
function schoolIcon(feature, latlng) {
  var redMarker = L.AwesomeMarkers.icon({
    icon: 'graduation-cap',
    markerColor: 'purple',
    prefix: 'fa',
    extraClasses: 'schools-icon',
  });
  return L.marker(latlng, { icon: redMarker })
}

function forRentIcon(feature, latlng) {
  var rentMarker = L.AwesomeMarkers.icon({
    icon: 'home',
    markerColor: 'lightred',
    prefix: 'fa',
    extraClasses: 'forrent-icon',
  });
  return L.marker(latlng, { icon: rentMarker })
}

function forSaleIcon(feature, latlng) {
  var saleMarker = L.AwesomeMarkers.icon({
    icon: 'home',
    markerColor: 'lightgreen',
    prefix: 'fa',
    extraClasses: 'forsale-icon',
  });
  return L.marker(latlng, { icon: saleMarker })
}

function bizIcon(feature, latlng) {
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
  if (!toggle) {
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
  if (!toggle) {
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
  if (!toggle) {
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
  if (!toggle) {
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
async function getSchools(lat, long) {

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

    request1.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request1.status == 200) {
        // Success!
        var data = JSON.parse(request1.responseText);
        resolve(data['schools'])

      } else if (request1.status <= 500) {
        // We reached our target server, but it returned an error

        console.log("unable to geocode! Response code: " + request1.status);
        var data = JSON.parse(request1.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request1.onerror = function () {
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
      var capped = e.charAt(0).toUpperCase() + e.slice(1);
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
          "Great Schools Rating": d.ratings['great_schools_rating'] || 'None',
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
        .attr('class', 'details-h2')
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

    request2.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request2.status == 200) {
        // Success!
        var data = JSON.parse(request2.responseText);
        // console.log(data['schools']);
        resolve(data.listings)

      } else if (request2.status <= 500) {
        // We reached our target server, but it returned an error

        console.log("unable to geocode! Response code: " + request2.status);
        var data = JSON.parse(request2.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request2.onerror = function () {
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

    request2.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request2.status == 200) {
        // Success!
        var data = JSON.parse(request2.responseText);
        // console.log(data['schools']);
        resolve(data.listings)

      } else if (request2.status <= 500) {
        // We reached our target server, but it returned an error

        console.log("unable to geocode! Response code: " + request2.status);
        var data = JSON.parse(request2.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request2.onerror = function () {
      // There was a connection error of some sort
      console.log("unable to connect to server");
    };

    request2.send();  // make the request
  });
};

// reverse geocode address

async function getAddress(lat, long) {
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

    request.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request.status == 200) {
        // Success!
        var data = JSON.parse(request.responseText);
        resolve(data.results[0].components.postcode);

      } else if (request.status <= 500) {
        // We reached our target server, but it returned an error

        console.log("unable to geocode! Response code: " + request.status);
        var data = JSON.parse(request.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request.onerror = function () {
      // There was a connection error of some sort
      console.log("unable to connect to server");
    };

    request.send();  // make the request
  });
};

//get buisness data
async function getbiz1(lat, lon) {

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

    request3.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request3.status == 200) {
        // Success!
        var data = JSON.parse(request3.responseText);
        // console.log(data['schools']);
        console.log(data);
        resolve(data.businesses)

      } else if (request3.status <= 500) {
        // We reached our target server, but it returned an error
        console.log(request3.responseText)
        console.log("unable to geocode! Response code: " + request3.status);
        var data = JSON.parse(request3.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request3.onerror = function () {
      // There was a connection error of some sort
      console.log("unable to connect to server");
    };

    request3.send();  // make the request
  });
};

//get buisness data
async function getbiz2(lat, lon) {

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

    request3.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request3.status == 200) {
        // Success!
        var data = JSON.parse(request3.responseText);
        // console.log(data['schools']);
        console.log(data);
        resolve(data.businesses)

      } else if (request3.status <= 500) {
        // We reached our target server, but it returned an error
        console.log(request3.responseText)
        console.log("unable to geocode! Response code: " + request3.status);
        var data = JSON.parse(request3.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request3.onerror = function () {
      // There was a connection error of some sort
      console.log("unable to connect to server");
    };

    request3.send();  // make the request
  });
};

//get buisness data
async function getbiz3(lat, lon) {

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

    request3.onload = function () {
      // see full list of possible response codes:
      // https://opencagedata.com/api#codes

      if (request3.status == 200) {
        // Success!
        var data = JSON.parse(request3.responseText);
        // console.log(data['schools']);
        console.log(data);
        resolve(data.businesses)

      } else if (request3.status <= 500) {
        // We reached our target server, but it returned an error
        console.log(request3.responseText)
        console.log("unable to geocode! Response code: " + request3.status);
        var data = JSON.parse(request3.responseText);
        console.log(data.status.message);
      } else {
        console.log("server error");
      }
    };
    request3.onerror = function () {
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
        .attr('class', 'details-h2')
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
        .attr('class', 'details-h2')
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
        .attr('class', 'details-h2')
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
var maxBounds = L.latLngBounds(
  L.latLng(5.499550, -167.276413),
  L.latLng(83.162102, -52.233040)
);

var stateLocs = {
  "AL": { "lat": 32.806671, "lon": -86.79113 },
  "AK": { "lat": 61.370716, "lon": -152.404419 },
  "AZ": { "lat": 33.729759, "lon": -111.431221 },
  "AR": { "lat": 34.969704, "lon": -92.373123 },
  "CA": { "lat": 36.116203, "lon": -119.681564 },
  "CO": { "lat": 39.059811, "lon": -105.311104 },
  "CT": { "lat": 41.597782, "lon": -72.755371 },
  "DE": { "lat": 39.318523, "lon": -75.507141 },
  "DC": { "lat": 38.897438, "lon": -77.026817 },
  "FL": { "lat": 27.766279, "lon": -81.686783 },
  "GA": { "lat": 33.040619, "lon": -83.643074 },
  "HI": { "lat": 21.094318, "lon": -157.498337 },
  "ID": { "lat": 44.240459, "lon": -114.478828 },
  "IL": { "lat": 40.349457, "lon": -88.986137 },
  "IN": { "lat": 39.849426, "lon": -86.258278 },
  "IA": { "lat": 42.011539, "lon": -93.210526 },
  "KS": { "lat": 38.5266, "lon": -96.726486 },
  "KY": { "lat": 37.66814, "lon": -84.670067 },
  "LA": { "lat": 31.169546, "lon": -91.867805 },
  "ME": { "lat": 44.693947, "lon": -69.381927 },
  "MD": { "lat": 39.063946, "lon": -76.802101 },
  "MA": { "lat": 42.230171, "lon": -71.530106 },
  "MI": { "lat": 43.326618, "lon": -84.536095 },
  "MN": { "lat": 45.694454, "lon": -93.900192 },
  "MS": { "lat": 32.741646, "lon": -89.678696 },
  "MO": { "lat": 38.456085, "lon": -92.288368 },
  "MT": { "lat": 46.921925, "lon": -110.454353 },
  "NE": { "lat": 41.12537, "lon": -98.268082 },
  "NV": { "lat": 38.313515, "lon": -117.055374 },
  "NH": { "lat": 43.452492, "lon": -71.563896 },
  "NJ": { "lat": 40.298904, "lon": -74.521011 },
  "NM": { "lat": 34.840515, "lon": -106.248482 },
  "NY": { "lat": 42.165726, "lon": -74.948051 },
  "NC": { "lat": 35.630066, "lon": -79.806419 },
  "ND": { "lat": 47.528912, "lon": -99.784012 },
  "OH": { "lat": 40.388783, "lon": -82.764915 },
  "OK": { "lat": 35.565342, "lon": -96.928917 },
  "OR": { "lat": 44.572021, "lon": -122.070938 },
  "PA": { "lat": 40.590752, "lon": -77.209755 },
  "RI": { "lat": 41.680893, "lon": -71.51178 },
  "SC": { "lat": 33.856892, "lon": -80.945007 },
  "SD": { "lat": 44.299782, "lon": -99.438828 },
  "TN": { "lat": 35.747845, "lon": -86.692345 },
  "TX": { "lat": 31.054487, "lon": -97.563461 },
  "UT": { "lat": 40.150032, "lon": -111.862434 },
  "VT": { "lat": 44.045876, "lon": -72.710686 },
  "VA": { "lat": 37.769337, "lon": -78.169968 },
  "WA": { "lat": 47.400902, "lon": -121.490494 },
  "WV": { "lat": 38.491226, "lon": -80.954453 },
  "WI": { "lat": 44.268543, "lon": -89.616508 },
  "WY": { "lat": 42.755966, "lon": -107.30249 },
};

if (document.cookie.split('=')[1] == undefined) {
  var state = "CA"
} else {
  var state = document.cookie.split('=')[1]
};


// mapid is the id of the div where the map will appear
var map = L
  .map('mapid')
  .fitBounds(maxBounds)
  .setView(new L.LatLng(stateLocs[state].lat, stateLocs[state].lon), 5.5); //testing purposess
  // .setView(new L.LatLng(37.689740802722724, -109.599609375), 5);
// .setView([47, 2], 10)
// .setView([40, -8025], 10);   // center position + zoom

// MAIN FUNCTION
map.on('click', async function (e) {
  alert("Lat, Lon : " + e.latlng.lat + ", " + e.latlng.lng) //for debugging
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
    id: 'Filter Views',
    tab: '<i class="fa fa-filter"></i>',
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
    id: 'user' + userid++,
    tab: '<i class="fa fa-user"></i>',
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
        type: "Point"
      }
    }
  ]

  var myStyle2 = {
    "color": "#ff7800",
    "weight": 400,
    "opacity": 0.65
  };

  L.geoJSON(data, { style: myStyle2 }
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
