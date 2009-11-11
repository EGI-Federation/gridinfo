<!--
	<script src="http://maps.google.com/maps?file=api&amp;v=2.x&amp;key=ABQIAAAAAKW6gFl6FivXLFVNFzbfjhRa_0exNNPAG0aUGAjusfNRdEZ1DhTBrCUvVP-YO4NHyI5eCdpz4CWnGg"
			type="text/javascript"></script>
    <script src='http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6.1'></script>
	<script src="http://api.maps.yahoo.com/ajaxymap?v=3.0&appid=euzuro-openlayers"></script>
-->

/*
            // Google Maps
            var gphy = new OpenLayers.Layer.Google(
            	"Google Physical",
            	{type: G_PHYSICAL_MAP}
            );
            var gmap = new OpenLayers.Layer.Google(
                "Google Streets", // the default
                {numZoomLevels: 20}
            );
            var ghyb = new OpenLayers.Layer.Google(
                "Google Hybrid",
                {type: G_HYBRID_MAP, numZoomLevels: 20}
            );
            var gsat = new OpenLayers.Layer.Google(
                "Google Satellite",
                {type: G_SATELLITE_MAP, numZoomLevels: 20}
            );
            map.addLayers([gphy, gmap, ghyb, gsat]);
            
            // create Virtual Earth layers
            var veroad = new OpenLayers.Layer.VirtualEarth(
                "Virtual Earth Roads",
                {'type': VEMapStyle.Road, 'sphericalMercator': true}
            );
            var veaer = new OpenLayers.Layer.VirtualEarth(
                "Virtual Earth Aerial",
                {'type': VEMapStyle.Aerial, 'sphericalMercator': true}
            );
            var vehyb = new OpenLayers.Layer.VirtualEarth(
                "Virtual Earth Hybrid",
                {'type': VEMapStyle.Hybrid, 'sphericalMercator': true}
            );
            map.addLayers([veroad, veaer, vehyb]);

            // create Yahoo layer
            var yahoo = new OpenLayers.Layer.Yahoo(
                "Yahoo Street",
                {'sphericalMercator': true}
            );
            var yahoosat = new OpenLayers.Layer.Yahoo(
                "Yahoo Satellite",
                {'type': YAHOO_MAP_SAT, 'sphericalMercator': true}
            );
            var yahoohyb = new OpenLayers.Layer.Yahoo(
                "Yahoo Hybrid",
                {'type': YAHOO_MAP_HYB, 'sphericalMercator': true}
            );
            map.addLayers([yahoo, yahoosat, yahoohyb]);
            
            // create Open Street Map and Open Aerial Map
            var mapnik = new OpenLayers.Layer.TMS("OpenStreetMap (Mapnik)",
                "http://tile.openstreetmap.org/",
                {
                    type: 'png', getURL: osm_getTileURL,
                    displayOutsideMaxExtent: true,
                    attribution: '<a href="http://www.openstreetmap.org/">OpenStreetMap</a>'
                }
            );            
            map.addLayers([mapnik]);
*/

function osm_getTileURL(bounds) {
    var res = this.map.getResolution();
    var x = Math.round((bounds.left - this.maxExtent.left) / (res * this.tileSize.w));
    var y = Math.round((this.maxExtent.top - bounds.top) / (res * this.tileSize.h));
    var z = this.map.getZoom();
    var limit = Math.pow(2, z);

    if (y < 0 || y >= limit) {
        return OpenLayers.Util.getImagesLocation() + "404.png";
    } else {
        x = ((x % limit) + limit) % limit;
        return this.url + z + "/" + x + "/" + y + "." + this.type;
    }
}