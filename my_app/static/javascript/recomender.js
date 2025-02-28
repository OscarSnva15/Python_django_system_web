async function initMap() {
    // Request needed libraries.
    const { Map } = await google.maps.importLibrary("maps");
    const myLatlng = {lat:19.617840149224154, lng:-99.30295140508093};
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: myLatlng,
    });
    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Da Click en el mapa para obtener las coordenadas de Latitud y Longitud!",
        position: myLatlng,
    });
    
    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
        position: mapsMouseEvent.latLng,
        });
        infoWindow.setContent(
        JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2),
        coordenadas.value = JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        );
        infoWindow.open(map);
    });
}
initMap();