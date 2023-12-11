// Initialize and add the map
let map;
let directionsService;
let directionsRenderer;

// info windows var
let hostelInfoWindow;
let campusEntranceInfoWindow;


//  function for infoWindow
function infoWindowFunction(url, name) {
  return `<a href="${url}"><h6>${name}</h6></a>`
}

async function initMap() {

  // campus main entrance coordinates
  const campusEntrancePosition = {lat: parseFloat(document.getElementById('campus-lat').value), 
                                  lng: parseFloat(document.getElementById('campus-lng').value) };
  // alert(campusEntrancePosition.lat)
  // The location of hostel
  const hostelPosition = {lat: parseFloat(document.getElementById('lat').value), 
                          lng: parseFloat(document.getElementById('lng').value) };

  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at hostel locaiton
  map = new Map(document.getElementById("map"), {
    zoom: 18,
    center: hostelPosition,
    gestureHandling: "greedy",
    mapId: "DEMO_MAP_ID",
    mapTypeId: 'satellite',
  });

 // Initialize Directions Service and Renderer
 directionsService = new google.maps.DirectionsService();
 directionsRenderer = new google.maps.DirectionsRenderer({
  polylineOptions: {
    strokeColor: '#FE9901', // Set the color of the direction line
    strokeWeight: 5
  },
  suppressMarkers: true,  // Show markers on the map
  // suppressPolylines: false // Show the polyline on the map

  });
 directionsRenderer.setMap(map);


   // open info windows
   hostelInfoWindow = new google.maps.InfoWindow({
    content: `<a href="${document.querySelector('#hostel-url').value}"><h6>${document.getElementById('hostel-name').value}</h6></a>`
  });

 campusEntranceInfoWindow = new google.maps.InfoWindow({
  content:`<h6>${document.getElementById('campus').value} Main Entrance</h6>`,
  });



  // Calculate and display directions immediately
  calculateAndDisplayRoute(campusEntrancePosition, hostelPosition);


    // The marker for campus entrance
const campusEntranceMarker = new AdvancedMarkerElement({
      map: map,
      position: campusEntrancePosition,
      // Customize the title to your taste
      title: `${document.getElementById('campus').value} Campus Entrance`,
    });
  

  // The marker, positioned at hostel
  const hostelMarker = new AdvancedMarkerElement({
    map: map,
    position: hostelPosition,
    // element: document.getElementById('hostel-name'),
    // the hostel name as title
    title:document.getElementById('hostel-name').value,
  });


  // Open info windows immediately
  hostelInfoWindow.open(map, hostelMarker);
  campusEntranceInfoWindow.open(map, campusEntranceMarker);




  // Add click event listener to the hostelMarker
  hostelMarker.addListener('click', () => {
  // Open the associated URL in a new tab or window
  window.location.href = document.getElementById('hostel-url').value;
  });
}

function calculateAndDisplayRoute(origin, destination) {
  const request = {
    origin: origin,
    destination: destination,
    travelMode: 'WALKING', //'WALKING', 'BICYCLING', etc.
  };

  directionsService.route(request, function (result, status) {
    if (status == 'OK') {
      directionsRenderer.setDirections(result);
    } else {
      alert('Error fetching directions:', status);
    }
  });
}

initMap();









// async function initMap() {
//   // campus main entrance coordinates
//   const campusEntrancePosition = {
//     lat: parseFloat(document.getElementById('campus-lat').value),
//     lng: parseFloat(document.getElementById('campus-lng').value),
//   };

//   // The location of hostel
//   const hostelPosition = {
//     lat: parseFloat(document.getElementById('lat').value),
//     lng: parseFloat(document.getElementById('lng').value),
//   };

//   // Request needed libraries.
//   //@ts-ignore
//   const { Map } = await google.maps.importLibrary('maps');
//   const { AdvancedMarkerElement } = await google.maps.importLibrary('marker');


 


//   // The marker, positioned at hostel location
//   const marker = new AdvancedMarkerElement({
//     map: map,
//     position: hostelPosition,
//     // the hostel name as title
//     title: document.getElementById('hostel-name').value,
//   });

//   // Add click event listener to the marker
//   marker.addListener('click', () => {
//     // Calculate and display directions when marker is clicked
//     calculateAndDisplayRoute(hostelPosition, campusEntrancePosition);
//   });
// }



// initMap();
