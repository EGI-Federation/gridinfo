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
            new OpenLayers.Control.KeyboardDefaults()
        ]
	};
    map = new OpenLayers.Map('map', options);

	/*********************************/
	/* Adding layers
	/*********************************/
    // OpenLayer WMS
    var olwms = new OpenLayers.Layer.WMS( "OpenLayers",
            "http://labs.metacarta.com/wms/vmap0", {layers: 'basic'} );
    map.addLayer(olwms);

    // OpenAerialMap
    var oam = new OpenLayers.Layer.WMS( "OpenStreetMap", 
     [
      "http://oam1.hypercube.telascience.org/tiles/",
      "http://oam2.hypercube.telascience.org/tiles/",
      "http://oam3.hypercube.telascience.org/tiles/"
     ],
         {layers: 'openaerialmap'}, {buffer: 1} );
    map.addLayer(oam);

    // NASA Global Mosaic
    var jpl_wms = new OpenLayers.Layer.WMS( "NASA Global Mosaic",
        "http://t1.hypercube.telascience.org/cgi-bin/landsat7", 
        {layers: "landsat7"});
    map.addLayer(jpl_wms);

    // NASA WMS
	var NASAwms = new OpenLayers.Layer.WMS( "NASA WMS",
		"http://wms.jpl.nasa.gov/wms.cgi?", {			
			layers: 'BMNG',
			format: 'image/png'},
		{isBaseLayer: true});
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
    var vector = new OpenLayers.Layer.Vector("Editable Vectors");
    map.addControl(new OpenLayers.Control.EditingToolbar(vector));
    //map.zoomToMaxExtent();
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
    var popup = new OpenLayers.Popup.FramedCloud("chicken", 
        feature.geometry.getBounds().getCenterLonLat(),
        new OpenLayers.Size(100,100),
        "<h2>"+feature.attributes.name + "</h2>" + feature.attributes.description,
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
