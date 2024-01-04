// Initialize and add the map
let map;
let directionsService;
let directionsRenderer;

// info windows var
let hostelInfoWindow;
let campusEntranceInfoWindow;
let selectedStartingPoint;

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
    mapTypeId: 'hybrid',
  });

  // Show notification on map load
  // showMapNotification("Map loaded successfully!");

 // Initialize Directions Service and Renderer
 directionsService = new google.maps.DirectionsService();
 directionsRenderer = new google.maps.DirectionsRenderer({
  polylineOptions: {
    strokeColor: '#FE9901', // Set the color of the direction line
    strokeWeight: 6
  },
  suppressMarkers: true,  // Show markers on the map
  // suppressPolylines: false // Show the polyline on the map

  });
 directionsRenderer.setMap(map);


   // open info windows
   hostelInfoWindow = new google.maps.InfoWindow({
    // content: `<a "><h6></h6></a>`
    content: `<a href="${document.querySelector('#hostel-url').value}" type="button" class="btn btn-warning">
    ${document.getElementById('hostel-name').value}
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-check" viewBox="0 0 16 16">
    <path d="M7.293 1.5a1 1 0 0 1 1.414 0L11 3.793V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v3.293l2.354 2.353a.5.5 0 0 1-.708.708L8 2.207l-5 5V13.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 2 13.5V8.207l-.646.647a.5.5 0 1 1-.708-.708z"/>
    <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m1.679-4.493-1.335 2.226a.75.75 0 0 1-1.174.144l-.774-.773a.5.5 0 0 1 .708-.707l.547.547 1.17-1.951a.5.5 0 1 1 .858.514Z"/>
    </svg>
    </a>`
  });


 campusEntranceInfoWindow = new google.maps.InfoWindow({
  content: `<button type="button" class="btn btn-primary">
  ${document.getElementById('campus').value} Main Entrance
  <i class="bi bi-signpost"></i>
  </button>`
  });



  // Calculate and display directions immediately
  calculateAndDisplayRoute(campusEntrancePosition, hostelPosition);


    // The marker for campus entrance
  const campusEntranceMarker = new AdvancedMarkerElement({
      map: map,
      position: campusEntrancePosition,
      // Customize the title to your taste
      title: `${document.getElementById('campus').value} Campus Entrance`,
      gmpDraggable: true,
    });
  

  // The marker, positioned at hostel
  const hostelMarker = new AdvancedMarkerElement({
    map: map,
    position: hostelPosition,
    // element: document.getElementById('hostel-name'),
    // the hostel name as title
    title:document.getElementById('hostel-name').value,
  });

  // Funtion for showing info window for campus 
  function openCampusInfo(info_window, map, marker) {

    info_window.open(map, marker);
    // Close the notification window after a certain duration (e.g., 3 seconds)
    setTimeout(() => {
      const newContent = `<button type="button" class="btn btn-primary">
      Move Red Marker To Set New Origin
      <i class="bi bi-signpost"></i>
      </button>`;
    info_window.setContent(newContent);
    }, 4000);
  }
  

  // Open info windows immediately
  hostelInfoWindow.open(map, hostelMarker);
  openCampusInfo(campusEntranceInfoWindow, map, campusEntranceMarker);
 

  ///////////////////EVENT LISTENERS///////////////////////////

  // Add click event listener to the hostelMarker
  hostelMarker.addListener('click', () => {
  // Open the associated URL in a new tab or window
  window.location.href = document.getElementById('hostel-url').value;
  });

  // Add dragend event listener to the marker
  campusEntranceMarker.addListener('dragend', function (event) {
    // Update the selectedStartingPoint when marker is dragged
    selectedStartingPoint = { lat: event.latLng.lat(), lng: event.latLng.lng() };
    
    // Recalculate and display route with the new starting point
    calculateAndDisplayRoute(selectedStartingPoint, hostelPosition);
    // showMapNotification("New Direction For Origin");

    changeWindowWhenMarkerMoves(campusEntranceInfoWindow, "New Origin")
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



function changeWindowWhenMarkerMoves(info_window, message) {
  const newContent = `<button type="button" class="btn btn-primary">
    ${message}
  <i class="bi bi-signpost"></i>
  </button>`;
  info_window.setContent(newContent);

  setTimeout(() => {
    const newContent = `<button type="button" class="btn btn-primary">
    Move Red Marker To Set New Origin
    <i class="bi bi-signpost"></i>
    </button>`;
  info_window.setContent(newContent);
  }, 3000);
}



function showMapNotification(message) {
  const notificationInfoWindow = new google.maps.InfoWindow({
    content: `<div class="alert alert-danger" role="alert">
        ${message}
  </div>`
  });

  notificationInfoWindow.setPosition(map.getCenter());
  notificationInfoWindow.open(map);
  // Close the notification window after a certain duration (e.g., 3 seconds)
  setTimeout(() => {
    notificationInfoWindow.close();
  }, 2000);
}


initMap();

