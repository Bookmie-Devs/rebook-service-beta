 // Initialize and add the map
let map;
let infoWindows = []; // Array to store InfoWindows
let directionsService;
// let directionsRenderer;
let campusEntranceInfoWindow;

 // campus main entrance coordinates
 const campusEntrancePosition = {lat: parseFloat(document.getElementById('campus-lat').value), 
                                lng: parseFloat(document.getElementById('campus-lng').value) };

//  function for infoWindow
 function infoWindowFunction(url, name) {
    // return ``
    return `<a type="button" class="btn btn-warning" href="${url}"
    style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
    ${name}
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-check" viewBox="0 0 16 16">
    <path d="M7.293 1.5a1 1 0 0 1 1.414 0L11 3.793V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v3.293l2.354 2.353a.5.5 0 0 1-.708.708L8 2.207l-5 5V13.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 2 13.5V8.207l-.646.647a.5.5 0 1 1-.708-.708z"/>
    <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m1.679-4.493-1.335 2.226a.75.75 0 0 1-1.174.144l-.774-.773a.5.5 0 0 1 .708-.707l.547.547 1.17-1.951a.5.5 0 1 1 .858.514Z"/>
    </svg>
    </a>`
 }

 async function initMap() {

 
 
   let jsonString = document.getElementById('hostel-coordinates').value
 
   jsonString = jsonString.replace(/None/g, 'null').replace(/'/g, '"');

   // Array of places (coordinates)
   const places = JSON.parse(jsonString)
 
   // Request needed libraries.
   //@ts-ignore
   const { Map } = await google.maps.importLibrary("maps");
   const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");


  // Initialize Directions Service and Renderer
  directionsService = new google.maps.DirectionsService();
  // directionsRenderer = new google.maps.DirectionsRenderer();

 
   // Center the map on the first place
   map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: campusEntrancePosition,
    gestureHandling: "greedy",
    mapTypeId: 'satellite',
    mapId: "DEMO_MAP_ID",
   });
   setTimeout(() => {
    map.setCenter(campusEntrancePosition)
    map.setZoom(18)
   }, 1200); 

 
 // Add markers for each place
 const markers = places.map(place => {
   const marker = new AdvancedMarkerElement({
    map: map,
    position: place,
    // the hostel name as title
    title: place.name, // Set the title for the marker (used as a tooltip)
   });

 
   // Create an info window for each marker
  const infoWindow = new google.maps.InfoWindow({
  content: infoWindowFunction(place.url, place.name),
  });
  
  // Store the InfoWindow in the array
  infoWindows.push(infoWindow);

 
   // Add click event listener to the marker
   marker.addListener('click', () => {
     // Open the associated URL in a new tab or window
     window.location.href = (place.url);
   });
 

   return marker;
 });

  // Open InfoWindows for each marker by default
  markers.forEach((marker, index) => {
    infoWindows[index].open(map, marker);
  });

  // Calculate and display directions for the campus entrance to each destination
  calculateAndDisplayRoutes(campusEntrancePosition, places);


  // The marker for campus entrance
  const campusEntranceMarker = new AdvancedMarkerElement({
    map: map,
    position: campusEntrancePosition,
    // Customize the title to your taste
    title: `${document.getElementById('campus').value} Campus Entrance`,
  });
    
  campusEntranceInfoWindow = new google.maps.InfoWindow({
    content: `<button type="button" class="btn btn-primary">
    ${document.getElementById('campus').value} Main Entrance
    <i class="bi bi-signpost"></i>
    </button>`
    });
  campusEntranceInfoWindow.open(map, campusEntranceMarker);
}



function calculateAndDisplayRoutes(origin, destinations) {
  destinations.forEach(destination => {
      const request = {
          origin: origin,
          destination: destination,
          travelMode: 'WALKING', // or other travel modes like 'BICYCLING', etc.
      };

      directionsService.route(request, function (result, status) {
          if (status === 'OK') {
              // Create a new DirectionsRenderer for each route
              const newRenderer = new google.maps.DirectionsRenderer({
                  polylineOptions: {
                      strokeColor: '#FE9901',
                      strokeWeight: 4,
                  },
                  preserveViewport: true,
                  suppressMarkers: true,
              });
              newRenderer.setMap(map);
              newRenderer.setDirections(result);
          } else {
              console.error('Error fetching directions:', status);
          }
      });
  });
}

 
 initMap();


















