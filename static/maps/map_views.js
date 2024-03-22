let map;
let infoWindows = [];
let directionsService;
let directionsRenderers = [];
let campusEntranceInfoWindow;
let colleges;

const campusEntrancePosition = {lat: parseFloat(document.getElementById('campus-lat').value), 
                                lng: parseFloat(document.getElementById('campus-lng').value) };
 function hostelInfoWindowFunction(url, category, name, pic_url, rooms_url, no_of_likes) {
  return `
    <div class="custom-card">
      <img src="${pic_url}" class="custom-card-img-top" alt="place.name">
      <div class="custom-card-body">
        <div  class="btn-container">
        <h5 class="custom-card-title">${name}</h5>
        <div class="love-container">
          <i class="bi bi-heart" id="icon"></i>
          <small>${no_of_likes}</small>
        </div>
        </div>
        <p class="custom-card-text">${category}</p>
        <div class="btn-container">
        <a href="${url}" class="custom-btn custom-btn-primary">Visit Hostel</a>
        <a href="${rooms_url}" class="custom-btn custom-btn-secondary">Book A Room</a>
        </div>
      </div>
    </div>
  `;
 }

 function collegeWindowFunction(url, name) {
  return `<a type="button"  class="btn btn-primary" href="${url}"
  style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .75rem;">
  From ${name}
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-geo-alt" viewBox="0 0 16 16">
  <path d="M12.166 8.94c-.524 1.062-1.234 2.12-1.96 3.07A32 32 0 0 1 8 14.58a32 32 0 0 1-2.206-2.57c-.726-.95-1.436-2.008-1.96-3.07C3.304 7.867 3 6.862 3 6a5 5 0 0 1 10 0c0 .862-.305 1.867-.834 2.94M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10"/>
  <path d="M8 8a2 2 0 1 1 0-4 2 2 0 0 1 0 4m0 1a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
  </svg>
  </a>`
}

function handleMarkerHover(map, marker, infoWindow) {
  marker.addListener('mouseover', () => {
    infoWindow.open(map, marker);
  });

  marker.addListener('mouseout', () => {
    infoWindow.close();
  });
}

 async function initMap() {
   let jsonString = document.getElementById('hostel-coordinates').value
   jsonString = jsonString.replace(/None/g, 'null').replace(/'/g, '"');
   const places = JSON.parse(jsonString)
   const { Map } = await google.maps.importLibrary("maps");
   const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  directionsService = new google.maps.DirectionsService();
  // directionsRenderer = new google.maps.DirectionsRenderer();
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
      mapTypeIds: ['roadmap','satellite'],
      style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
      position: google.maps.ControlPosition.TOP_CENTER,},
   });
   setTimeout(() => {
    map.setCenter(campusEntrancePosition)
    map.setZoom(15)
   }, 1200); 
  //  const buttons = [
  //   // ["<", "rotate", 20, google.maps.ControlPosition.LEFT_CENTER],
  //   // [">", "rotate", -20, google.maps.ControlPosition.RIGHT_CENTER],
  //   ["Tilt Down", "tilt", 20, google.maps.ControlPosition.TOP_LEFT],
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
  //     // case "tilt":
  //     //   map.setTilt(map.getTilt() + amount);
  //     //   break;
  //     case "rotate":
  //       map.setHeading(map.getHeading() + amount);
  //       break;
  //     default:
  //       break;
  //   }
  // };

 const markers = places.map(place => {
   const marker = new AdvancedMarkerElement({
    map: map,
    position: place,
    content: hostelMarkerContent(`${place.name}`),
    title: place.name, // Set the title for the marker (used as a tooltip)
   });

  const infoWindow = new google.maps.InfoWindow({
  content: hostelInfoWindowFunction(place.url, place.category ,place.name, place.pic_url, place.rooms_url, place.no_of_likes),
  });
  infoWindows.push(infoWindow);

  marker.addListener('click', () => {
    //  window.location.href = (place.url);
    infoWindow.open(map, marker);
    setTimeout(() => {
      infoWindow.close()
    }, 5000);
   });

  // Call functions to handle marker events
  handleMarkerHover(map, marker, infoWindow);
  // handleMarkerClick(marker, place.url);

   return marker;
  });
  // markers.forEach((marker, index) => {
  //   infoWindows[index].open(map, marker);
  // });
  const campusEntranceMarker = new AdvancedMarkerElement({
    map: map,
    position: campusEntrancePosition,
    content: originMarkerContent(`${document.getElementById('campus').value} Main Entrance`),
    title: `${document.getElementById('campus').value} Campus Entrance`,
  });
  calculateAndDisplayRoutes(campusEntrancePosition, places, map);
  // campusEntranceInfoWindow = new google.maps.InfoWindow({
  //   content: `<button type="button" class="btn btn-primary">
  //   ${document.getElementById('campus').value} Main Entrance
  //   <i class="bi bi-signpost"></i>
  //   </button>`
  //   });
  // campusEntranceInfoWindow.open(map, campusEntranceMarker);
let previousMarker = null;
let previousInfoWindow = null;

colleges = document.getElementById('colleges');

colleges.addEventListener('change', (event) => {
  const selectedOption = colleges.options[colleges.selectedIndex];

  if (selectedOption) {
    if (selectedOption.value==""){
      calculateAndDisplayRoutes(campusEntrancePosition, places, map);
      if (previousMarker) {
        previousMarker.setMap(null);
        previousMarker = null;
      }
      campusEntranceMarker.setMap(map)
      map.setCenter(campusEntrancePosition);
    }
    else{
    const collegeCoordinate = parseCoordinate(selectedOption.value);

    campusEntranceMarker.setMap(null)
    if (previousMarker) {
      previousMarker.setMap(null);
      previousMarker = null;
    }
    if (previousInfoWindow) {
      previousInfoWindow.close();
      previousInfoWindow = null;
    }
    const collegeEntranceMarker = new AdvancedMarkerElement({
      map: map,
      position: collegeCoordinate,
      content: originMarkerContent(`From ${selectedOption.innerText}`),
      title: `${selectedOption.innerText}`,
    });

    const infoWindow = new google.maps.InfoWindow({
      content: collegeWindowFunction("#", selectedOption.innerText),
    });
    map.setCenter(collegeCoordinate);
    previousMarker = collegeEntranceMarker;
    previousInfoWindow = infoWindow;

    calculateAndDisplayRoutes(collegeCoordinate, places, map);
  }}
  });
}

function calculateAndDisplayRoutes(origin, destinations, map) {
  clearDirectionsRenderers()
  destinations.forEach(destination => {
      const request = {
          origin: origin,
          destination: destination,
          travelMode: 'WALKING',
      };
      directionsService.route(request, function (result, status) {
          if (status === 'OK') {
              const newRenderer = new google.maps.DirectionsRenderer({
                  polylineOptions: {
                    strokeOpacity: 1.0,
                    strokeColor: '#FE9901',
                    strokeWeight: 4,
                  },
                  preserveViewport: true,
                  suppressMarkers: true,
              });
              newRenderer.setMap(map);
              newRenderer.setDirections(result);
            directionsRenderers.push(newRenderer);

            const durationInSeconds = result.routes[0].legs[0].duration.value;
            const durationInMinutes = Math.round(durationInSeconds / 60);
          } else {
              console.error('Error fetching directions:', status);
          }
      });
  });
}

function parseCoordinate(coordinateString) {

  const {lat, lng} = JSON.parse(coordinateString.replace(/None/g, 'null').replace(/'/g, '"'))

  return {lat:parseFloat(lat), lng:parseFloat(lng)}
}

function clearDirectionsRenderers() {
  directionsRenderers.forEach(renderer => {
    renderer.setMap(null);
  });
  directionsRenderers = [];
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

 initMap();

 export {parseCoordinate, collegeWindowFunction}

window.addEventListener('load', ()=>{
  document.getElementById('d').showModal()
})

  document.querySelector('.load').style.display = "flex";
  // setTimeout(function () {
  // }, 4000);
  
  setInterval(() => {
    if (document. readyState === 'complete') {
     document.querySelector('.load').style.display = 'none';
     clearInterval(stateCheck);  
    } 
  }, 100);








