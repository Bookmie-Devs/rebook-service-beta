// Initialize and add the map
let map;

async function initMap() {

  // campus main entrance coordinates
  const campusEntrancePosition = { lat: parseFloat(document.getElementById('campus-lat').value), 
                                  lng: parseFloat(document.getElementById('campus-lng').value) };
  // alert(campusEntrancePosition.lat)
  // The location of hostel
  const hostelPosition = { lat: parseFloat(document.getElementById('lat').value), 
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

  // The marker, positioned at Uluru
  const marker = new AdvancedMarkerElement({
    map: map,
    position: hostelPosition,
    // the hostel name as title
    title:document.getElementById('hostel-name').value,
  });

  // Add click event listener to the marker
  marker.addListener('click', () => {
  // Open the associated URL in a new tab or window
  window.location.href = document.getElementById('hostel-url').value;
  });

}

initMap();