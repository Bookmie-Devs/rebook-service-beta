// Initialize and add the map
let map;

async function initMap() {

  // The location of hostel
  const position = { lat: parseFloat(document.getElementById('lat').value), 
                     lng: parseFloat(document.getElementById('lng').value) };

  // Request needed libraries.
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");
  const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

  // The map, centered at hostel locaiton
  map = new Map(document.getElementById("map"), {
    zoom: 18,
    center: position,
    mapId: "DEMO_MAP_ID",
    mapTypeId: 'satellite',
  });

  // The marker, positioned at Uluru
  const marker = new AdvancedMarkerElement({
    map: map,
    position: position,
    // the hostel name as title
    title:document.getElementById('hostel-name').value,
  });
}

initMap();