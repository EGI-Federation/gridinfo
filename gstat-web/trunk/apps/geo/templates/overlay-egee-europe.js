function execOverlay() {
    // Set it in the center of europe
	map.setCenter(new OpenLayers.LonLat(11, 47.5), 4.5);

	// Create popups
	{% for name, lon, lat, html in popups %}
	popup = new OpenLayers.Popup("{{name}}",
	                             new OpenLayers.LonLat({{lon}},{{lat}}),
	                             new OpenLayers.Size(50, 60),
	                             "{% autoescape off %}{{html}}{% endautoescape %}",
	                             false);
	popup.opacity = 0.9;
	map.addPopup(popup);
	{% endfor %}	
}