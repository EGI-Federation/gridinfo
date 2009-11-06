// making these global variables so it is easy for debugging/inspecting -Firebug
var map, select, sundials;

// avoid pink tiles
OpenLayers.IMAGE_RELOAD_ATTEMPTS = 3;
OpenLayers.Util.onImageLoadErrorColor = "transparent";

/*********************************/
/* Openlayers main function
/*********************************/
function init(){

	/*********************************/
	/* Map setup
	/*********************************/
	var options = {
        controls: [
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            new OpenLayers.Control.LayerSwitcher(),
            new OpenLayers.Control.Scale(),
            new OpenLayers.Control.ScaleLine(),
            new OpenLayers.Control.Permalink(),
            new OpenLayers.Control.MousePosition(),
            new OpenLayers.Control.OverviewMap(),
            new OpenLayers.Control.Attribution()
        ]
	};
    map = new OpenLayers.Map('map', options);
    map.fractionalZoom = true;

	/*********************************/
	/* Adding layers
	/*********************************/
	// Attribution
	attribution = 'Provided by <a href="https://svnweb.cern.ch/trac/gridinfo/">GStat 2.0</a>';

    // OpenLayer WMS
    var olwms = new OpenLayers.Layer.WMS( "OpenLayers",
            "http://labs.metacarta.com/wms/vmap0",
            {layers: 'basic'},
            {'attribution': attribution} );
    map.addLayer(olwms);

    // NASA WMS
	var NASAwms = new OpenLayers.Layer.WMS( "NASA WMS",
		"http://wms.jpl.nasa.gov/wms.cgi?", {			
			layers: 'BMNG',
			format: 'image/png'},
		{isBaseLayer: true, 'attribution': attribution});
	map.addLayer(NASAwms);

	/*********************************/
	/* Adding overlays for Grid Sites
	/*********************************/
    // KML from The Grid
    sundials = new OpenLayers.Layer.Vector("The Grid", {
        projection: map.displayProjection,
        strategies: [new OpenLayers.Strategy.Fixed()],
        protocol: new OpenLayers.Protocol.HTTP({
            url: "/gstat/geo/kml",
            format: new OpenLayers.Format.KML({
                extractStyles: true,
                extractAttributes: true
            })
        })
    });
    map.addLayer(sundials)

	/*********************************/
	/* Adding popups
	/* See popup functions below
	/*********************************/
    // Popups
    select = new OpenLayers.Control.SelectFeature(sundials);
    sundials.events.on({
        "featureselected": onFeatureSelect,
        "featureunselected": onFeatureUnselect
    });
    map.addControl(select);
    select.activate();

	/*********************************/
	/* Final setup - center and zoom
	/*********************************/
//    var vector = new OpenLayers.Layer.Vector("Editable Vectors");
//    map.addControl(new OpenLayers.Control.EditingToolbar(vector));
    if (!map.getCenter()) map.setCenter(new OpenLayers.LonLat(5, 15), 2);
}


/*********************************/
/* Openlayers popup functions
/*********************************/
function onPopupClose(evt) {
    select.unselectAll();
}

function onFeatureSelect(event) {
    var feature = event.feature;
    var selectedFeature = feature;
    var msg = "<h2>" + feature.attributes.name + "</h2>" +
            '<p>' + feature.attributes.description + '</p>' + 
            '<p><a href="/gstat/site/' + feature.attributes.name + '">Summary View</a></p>';
    var popup = new OpenLayers.Popup.FramedCloud("chicken", 
        feature.geometry.getBounds().getCenterLonLat(),
        new OpenLayers.Size(100,100), msg,
        null, true, onPopupClose
    );
    popup.panMapIfOutOfView = false;
    feature.popup = popup;
    map.addPopup(popup);
}

function onFeatureUnselect(event) {
    var feature = event.feature;
    if(feature.popup) {
        map.removePopup(feature.popup);
        feature.popup.destroy();
        delete feature.popup;
    }
}
