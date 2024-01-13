// import { parseCoordinate } from "./map_views";
// Initialize and add the map
let map;
let directionsService;
let directionsRenderer;
// info windows var
let hostelInfoWindow;
let campusEntranceInfoWindow;
let selectedStartingPoint;
let colleges;

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
    zoom: 15,
    center: campusEntrancePosition,
    gestureHandling: "greedy",
    // mapId: "DEMO_MAP_ID",
    mapId: "90f87356969d889c",
    // heading: -195,
    // tilt: 60,
    mapTypeId:"satellite",
    streetViewControl: false,
    zoomControl: false,
    mapTypeControl: true,
    mapTypeControlOptions: {
      mapTypeIds: ['roadmap','satellite','hybrid'],
      style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
      position: google.maps.ControlPosition.TOP_CENTER,},
  });
  
  setTimeout(() => {
    map.setCenter(campusEntrancePosition)
    map.setZoom(16)
  }, 1200);


  // Show notification on map load
  // showMapNotification("Map loaded successfully!");

  const buttons = [
    ["<", "rotate", 20, google.maps.ControlPosition.LEFT_CENTER],
    [">", "rotate", -20, google.maps.ControlPosition.RIGHT_CENTER],
    // ["Tilt Down", "tilt", 20, google.maps.ControlPosition.TOP_CENTER],
    // ["Tilt Up", "tilt", -20, google.maps.ControlPosition.BOTTOM_CENTER],
  ];

  buttons.forEach(([text, mode, amount, position]) => {
    const controlDiv = document.createElement("div");
    const controlUI = document.createElement("button");

    controlUI.classList.add("ui-button");
    controlUI.innerText = `${text}`;
    controlUI.addEventListener("click", () => {
      adjustMap(mode, amount);
    });
    controlDiv.appendChild(controlUI);
    map.controls[position].push(controlDiv);
  });

  const adjustMap = function (mode, amount) {
    switch (mode) {
      // case "tilt":
      //   map.setTilt(map.getTilt() + amount);
      //   break;
      case "rotate":
        map.setHeading(map.getHeading() + amount);
        break;
      default:
        break;
    }
  };



 // Initialize Directions Service and Renderer
 directionsService = new google.maps.DirectionsService();
 directionsRenderer = new google.maps.DirectionsRenderer({
  polylineOptions: {
    strokeColor: '#FE9901', 
    strokeWeight: 6
  },
  preserveViewport: true,
  suppressMarkers: true,  // Show markers on the map
  // suppressPolylines: false // Show the polyline on the map

  });
 directionsRenderer.setMap(map);

  // open info windows
  hostelInfoWindow = new google.maps.InfoWindow({
    content: `<a href="${document.querySelector('#hostel-url').value}" type="button" class="btn btn-warning">
    ${document.getElementById('hostel-name').value}
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-house-check" viewBox="0 0 16 16">
    <path d="M7.293 1.5a1 1 0 0 1 1.414 0L11 3.793V2.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v3.293l2.354 2.353a.5.5 0 0 1-.708.708L8 2.207l-5 5V13.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 2 13.5V8.207l-.646.647a.5.5 0 1 1-.708-.708z"/>
    <path d="M12.5 16a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7m1.679-4.493-1.335 2.226a.75.75 0 0 1-1.174.144l-.774-.773a.5.5 0 0 1 .708-.707l.547.547 1.17-1.951a.5.5 0 1 1 .858.514Z"/>
    </svg>
    </a>`
  });


 campusEntranceInfoWindow = new google.maps.InfoWindow({
  content: `<button type="button" class="btn btn-success">
  ${document.getElementById('campus').value} Main Entrance
  <i class="bi bi-signpost"></i>
  </button>`
  });

  
  // Calculate and display directions immediately
  calculateAndDisplayRoute(campusEntrancePosition, hostelPosition, directionsRenderer);

    // The marker for campus entrance
  const campusEntranceMarker = new AdvancedMarkerElement({
      map: map,
      position: campusEntrancePosition,
      content: originMarkerContent(`${document.getElementById('campus').value} Entrance`),
      title: 'Origin',
      gmpDraggable: true,
    });
  
  // The marker, positioned at hostel
  const hostelMarker = new AdvancedMarkerElement({
    map: map,
    position: hostelPosition,
    content: hostelMarkerContent(document.getElementById('hostel-name').value),
    // element: document.getElementById('hostel-name'),
    // the hostel name as title
    title:document.getElementById('hostel-name').value,
  });

  // Funtion for showing info window for campus 
  // function openCampusInfo(info_window, map, marker) {

  //   info_window.open(map, marker);
  //   // Close the notification window after a certain duration (e.g., 3 seconds)
  //   setTimeout(() => {
  //     const newContent = `<button type="button" class="btn btn-primary"
  //     style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
  //     Move Marker To Change Origin
  //     <i class="bi bi-signpost"></i>
  //     </button>`;
  //   info_window.setContent(newContent);
  //   }, 3000);
  // }
  

  // Open info windows immediately
  // hostelInfoWindow.open(map, hostelMarker);
  // openCampusInfo(campusEntranceInfoWindow, map, campusEntranceMarker);
 

  ///////////////////EVENT LISTENERS///////////////////////////

  // Add click event listener to the hostelMarker
  hostelMarker.addListener('click', () => {
  // Open the associated URL in a new tab or window
  window.location.href = document.getElementById('hostel-url').value;
  });

  // dragend event listener to the marker
  campusEntranceMarker.addListener('dragend', function (event) {
    // Update the selectedStartingPoint when marker is dragged
    selectedStartingPoint = { lat: event.latLng.lat(), lng: event.latLng.lng() };
    // campusEntranceMarker.setContent(originMarkerContent("sjd"))
    // Recalculate and display route with the new starting point
    calculateAndDisplayRoute(selectedStartingPoint, hostelPosition, directionsRenderer);

  });


  let previousMarker = null;
  // let previousInfoWindow = null;

  colleges = document.getElementById('colleges');

  colleges.addEventListener('change', (event) => {
  // Get the selected option
  const selectedOption = colleges.options[colleges.selectedIndex];

  // Check if an option is selected
  if (selectedOption) {
    if (selectedOption.value==""){
      calculateAndDisplayRoute(campusEntrancePosition, hostelPosition, directionsRenderer);
      if (previousMarker) {
        previousMarker.setMap(null);
        previousMarker = null;
      }
      campusEntranceMarker.setMap(map)
      map.setCenter(campusEntrancePosition);
    }
    else{
    campusEntranceMarker.setMap(null)
    const collegeCoordinate = parseCoordinate(selectedOption.value);

    // Remove previous marker and info window if they exist
    if (previousMarker) {
      previousMarker.setMap(null);
      previousMarker = null;
    }

    // if (previousInfoWindow) {
    //   previousInfoWindow.close();
    //   previousInfoWindow = null;
    // }

    // Create new marker and info window
    const collegeEntranceMarker = new AdvancedMarkerElement({
      map: map,
      position: collegeCoordinate,
      content: originMarkerContent(`${selectedOption.innerText}`),
      // Customize the title to your taste
      title: `${selectedOption.innerText}`,
    });

    // const infoWindow = new google.maps.InfoWindow({
    //   content: collegeWindowFunction("#", selectedOption.innerText),
    // });

    map.setCenter(collegeCoordinate);

    // infoWindow.open(map, collegeEntranceMarker);
    // Store the new marker and info window
    previousMarker = collegeEntranceMarker;
    // previousInfoWindow = infoWindow;

    // Get the inner text of the selected option
    calculateAndDisplayRoute(collegeCoordinate, hostelPosition, directionsRenderer);
  }}
  });
}

// Function for infoWindow
function infoWindowFunction(url, name) {
  return `<a href="${url}"><h6>${name}</h6></a>`
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

function calculateAndDisplayRoute(origin, destination, directionsRenderer) {
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


function changeWindowWhenMarkerMoves(message) {
  originMarkerContent(message);
  setTimeout(() => {
  const newContent = 'Move Marker To Change Origin'
  originMarkerContent(newContent);
  }, 3000);
}

function originMarkerContent(textContent) {
  const content = document.createElement("div");
  content.className = "origin-marker-content";
  content.textContent = textContent;
  return content
}
 

function hostelMarkerContent(textContent) {
  const content = document.createElement("div");
  content.className = "hostel-marker-content";
  content.textContent = textContent;

  return content
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

function parseCoordinate(coordinateString) {
  const {lat, lng} = JSON.parse(coordinateString.replace(/'/g, '"'))

  return {lat:parseFloat(lat), lng:parseFloat(lng)}
}

initMap();

