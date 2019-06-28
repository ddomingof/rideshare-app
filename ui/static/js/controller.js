$(document).ready(function () {


    var map = L.map('map').setView([21.038576,75.0582583], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {}).addTo(map);

    var myHouse = L.marker([21.038576,75.0582583]);

    myHouse.addTo(map)
        .bindPopup('Meeting Point.')
        .openPopup();

    function onMapClick(e) {

        // Update value in input
        $('#endDest').val(e.latlng.toString().replace("LatLng(", "").replace(")", ""));

        // Show in form
        $('#endPlace').html(e.latlng.toString().replace("LatLng(", "").replace(")", ""));

        // Remove destination marker in order to update it
        if (typeof destMarker !== 'undefined') {
            destMarker.remove();
        }

        destMarker = L.marker(e.latlng);

        destMarker.addTo(map)
            .bindPopup('Selected Destination')
            .openPopup();
    }

    map.on('dblclick', onMapClick);

    $('#startDest').val([50.748547, 7.200279]);

});
