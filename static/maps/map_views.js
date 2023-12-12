 // Initialize and add the map
 let map;
 let infoWindows = []; // Array to store InfoWindows

//  function for infoWindow
 function infoWindowFunction(url, name) {
    // return ``
    return `<a type="button" class="btn btn-warning" href="${url}">${name}
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
 
   // Center the map on the first place
   map = new Map(document.getElementById("map"), {
     zoom: 15,
    center: places[0],
    gestureHandling: "greedy",
     mapTypeId: 'satellite',
     mapId: "DEMO_MAP_ID",
   });

 
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
  

}
 
 initMap();