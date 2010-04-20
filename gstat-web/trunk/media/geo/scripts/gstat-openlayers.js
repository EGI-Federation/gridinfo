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
	var attribution = 'Provided by <a href="https://svnweb.cern.ch/trac/gridinfo/">GStat 2.0</a>';

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
            '<p><a href="/gstat/site/' + feature.attributes.name + '">Site View</a></p>';
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

/*********************************/
/* Geo View functions
/*********************************/
function changeFilterValue(event) {
    var filtertype = document.getElementById('filtertype');
    var filtervalue = document.getElementById('filtervalue');
    if (filtertype.value == 'none') {
        while (filtervalue.length > 0) {
	        filtervalue.remove(0);
	    }
	    map.removeLayer(sundials);
        sundials = new OpenLayers.Layer.Vector("The Grid");
        map.addLayer(sundials);
    } else {
    	updateFullScreenLink();
        var kmllink = document.getElementById('kmllink');
        var kmlurl = "/gstat/geo/kml/" + filtertype.value + '/' + filtervalue.value;
        kmllink.href = kmlurl;
        map.removeLayer(sundials);
        sundials = new OpenLayers.Layer.Vector("The Grid", {
            projection: map.displayProjection,
            strategies: [new OpenLayers.Strategy.Fixed()],
            protocol: new OpenLayers.Protocol.HTTP({
                url: kmlurl,
                format: new OpenLayers.Format.KML({
                    extractStyles: true,
                    extractAttributes: true
                })
            })
        });
        map.addLayer(sundials);
	    select = new OpenLayers.Control.SelectFeature(sundials);
	    sundials.events.on({
	        "featureselected": onFeatureSelect,
	        "featureunselected": onFeatureUnselect
	    });
	    map.addControl(select);
	    select.activate();
    }
    window.location.hash ='#/' + encodeURIComponent(filtertype.value) +
                          '/' + encodeURIComponent(filtervalue.value);
    return true;
}

function changeOverlayType(event) {
    updateFullScreenLink();
    var overlaytype = document.getElementById('overlaytype').value;
    if (overlaytype == 'filters') {
        var max = map.popups.length;
	    for (var i=max-1; i>=0; i--) {
	        map.removePopup(map.popups[i]);
	    }
    } else {
        var url = '/gstat/geo/overlay/' + overlaytype;
        var Y = YUI();
        var objTransaction = Y.Get.script(url,
                                            { onSuccess: function() {
                                                execOverlay();
                                            }});
    }
}

function updateFullScreenLink(){
    var fullscreenlink = document.getElementById('fullscreenlink');
    var filtertype = document.getElementById('filtertype');
    var filtervalue = document.getElementById('filtervalue');
    var kmlurl = "/gstat/geo/kml/" + filtertype.value + '/' + filtervalue.value;
    var overlaytype = document.getElementById('overlaytype').value;
    var overlayurl = "/gstat/geo/overlay/" + overlaytype
    var fullscreenurl = "/gstat/geo/openlayers/fullscreen"
    		+ "?kml=" + encodeURIComponent(kmlurl) 
    		+ "&overlay=" + encodeURIComponent(overlayurl);
    fullscreenlink.href = fullscreenurl;
}

function changeURL(event) {
    var filtertype = document.getElementById('filtertype');
    var filtervalue = document.getElementById('filtervalue');
    var value = event.value.substring(1, event.value.length);
    var slashpos = value.search("/");
    filtertype.value = value.substring(0, slashpos);
    changeFilterType(event);
    filtervalue.value = value.substring(slashpos+1, value.length);
    changeFilterValue(event);        
}
