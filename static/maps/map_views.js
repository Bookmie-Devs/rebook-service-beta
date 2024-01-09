 // Initialize and add the map
let map;
let infoWindows = []; // Array to store InfoWindows
let directionsService;
let directionsRenderers = [];
let campusEntranceInfoWindow;
let colleges;
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

 function collegeWindowFunction(url, name) {
  // return ``
  return `<a type="button"  class="btn btn-primary" href="${url}"
  style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
  From ${name}
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
  <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A32 32 0 0 1 8 14.58a32 32 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10"/>
  <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4m0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
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
    // heading: -180,
    streetViewControl: false,
    // tilt: 36.6,
    gestureHandling: "greedy",
    mapTypeId: 'satellite',
    mapId: "90f87356969d889c",
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
      position: google.maps.ControlPosition.TOP_CENTER,},
      
   });
   setTimeout(() => {
    map.setCenter(campusEntrancePosition)
    map.setZoom(17)
   }, 1200); 

  //  const buttons = [
  //   ["Rotate Left", "rotate", 20, google.maps.ControlPosition.LEFT_CENTER],
  //   ["Rotate Right", "rotate", -20, google.maps.ControlPosition.RIGHT_CENTER],
  //   ["Tilt Down", "tilt", 20, google.maps.ControlPosition.BOTTOM_CENTER],
  //   ["Tilt Up", "tilt", -20, google.maps.ControlPosition.TOP_CENTER],
  // ];

  // buttons.forEach(([text, mode, amount, position]) => {
  //   const controlDiv = document.createElement("div");
  //   const controlUI = document.createElement("button");

  //   controlUI.classList.add("ui-button");
  //   controlUI.innerText = `${text}`;
  //   controlUI.addEventListener("click", () => {
  //     adjustMap(mode, amount);
  //   });
  //   controlDiv.appendChild(controlUI);
  //   map.controls[position].push(controlDiv);
  // });

  // const adjustMap = function (mode, amount) {
  //   switch (mode) {
  //     case "tilt":
  //       map.setTilt(map.getTilt() + amount);
  //       break;
  //     case "rotate":
  //       map.setHeading(map.getHeading() + amount);
  //       break;
  //     default:
  //       break;
  //   }
  // };

   
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
  calculateAndDisplayRoutes(campusEntrancePosition, places, map);


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

let previousMarker = null;
let previousInfoWindow = null;

colleges = document.getElementById('colleges');

colleges.addEventListener('change', (event) => {
  // Get the selected option
  const selectedOption = colleges.options[colleges.selectedIndex];

  // Check if an option is selected
  if (selectedOption) {
    const collegeCoordinate = parseCoordinate(selectedOption.value);

    // Remove previous marker and info window if they exist
    if (previousMarker) {
      previousMarker.setMap(null);
      previousMarker = null;
    }

    if (previousInfoWindow) {
      previousInfoWindow.close();
      previousInfoWindow = null;
    }

    // Create new marker and info window
    const collegeEntranceMarker = new AdvancedMarkerElement({
      map: map,
      position: collegeCoordinate,
      // Customize the title to your taste
      title: `${selectedOption.innerText}`,
    });

    const infoWindow = new google.maps.InfoWindow({
      content: collegeWindowFunction("#", selectedOption.innerText),
    });

    map.setCenter(collegeCoordinate);

    infoWindow.open(map, collegeEntranceMarker);
    // Store the new marker and info window
    previousMarker = collegeEntranceMarker;
    previousInfoWindow = infoWindow;

    // Get the inner text of the selected option
    calculateAndDisplayRoutes(collegeCoordinate, places, map);
  }
  });
}



function calculateAndDisplayRoutes(origin, destinations, map) {
  clearDirectionsRenderers()
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

            // Store the DirectionsRenderer in an array in to
            // be able to clear it 
            directionsRenderers.push(newRenderer);
          } else {
              console.error('Error fetching directions:', status);
          }
      });
  });
}

function parseCoordinate(coordinateString) {
  const {lat, lng} = JSON.parse(coordinateString.replace(/'/g, '"'))

  return {lat:parseFloat(lat), lng:parseFloat(lng)}
}

function clearDirectionsRenderers() {
  // Remove all existing DirectionsRenderers from the map
  directionsRenderers.forEach(renderer => {
    renderer.setMap(null);
  });
  // Clear the array
  directionsRenderers = [];
}


function changeOriginToCollege() {
    // Get the selected option element
    const selectedOption = document.getElementById('colleges').options[document.getElementById('colleges').selectedIndex];

    // Check if an option is selected
    if (selectedOption) {
      // Get the value of the selected option
      const selectedValue = selectedOption.value;

      // Use the selectedValue as needed
      console.log('Selected Value:', selectedValue);
    }
}
 
 initMap();


















