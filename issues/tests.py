from django.test import TestCase

# Create your tests here.
'''<script>
    // Latitude aur Longitude values ko direct use kiya gaya hai
    var latitude = {{ issue.latitude }};
    var longitude = {{ issue.longitude }};

    // Yeh check lagana zaroori hai ki coordinates numbers hain, null nahi.
    if (typeof latitude === 'number' && typeof longitude === 'number' && latitude !== null && longitude !== null) {
        
        // Map Initialize
        var map = L.map('mapid').setView([latitude, longitude], 15); // 15 is zoom level

        // Tile Layer (Map visuals)
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Marker at Issue Location
        L.marker([latitude, longitude]).addTo(map)
            .bindPopup("<b>Issue Location</b>")
            .openPopup();
    } 
    // Agar coordinates nahi mile, toh Map initialize nahi hoga aur koi error bhi nahi aayega.
</script>'''