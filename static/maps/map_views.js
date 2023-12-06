 // Initialize and add the map
 let map;
 let infoWindows = []; // Array to store InfoWindows

//  function for infoWindow
 function infoWindowFunction(url, name) {
    return `<a href="${url}"><h6>${name}</h6></a>`
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
     zoom: 16,
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