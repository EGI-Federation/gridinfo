// This file is part of the GridMap software (see http://gridmap.cern.ch)
// Copyright (c) EDS and CERN 2007, patent pending
//
// Author: Max Boehm, max.boehm@eds.com, max.boehm@cern.ch
//
// History:
// 18.09.2007  mb        first internal version
// 19.10.2007  mb        1st deployed version, showed at EGEE'07 conference
// 25.11.2007  mb        release v01, complete overwork, colorkey functions added
// 24.02.2009  lk/mb     sticky tooltips no longer disappear when mouse is moved over sitenames
//                       jsgraphics extension fillRect1() moved into this file
//

// needs:
// - wz_jsgraphics.js
// - wz_tooltip_mb.js

// extend the jsgraphics library
jsGraphics.prototype.fillRect1 = function(x, y, w, h, addstr, text)
{
    this.htm += '<div '+addstr+' style="position:absolute;overflow:hidden;left:'+x+'px;top:'+y+
        'px;width:'+w+'px;height:'+h+'px;'+'clip:rect(0,'+w+'px,'+h+'px,0);background-color:'+this.color+
        ';text-align:center;white-space:nowrap;font-family:'+this.ftFam+';font-size:'+this.ftSz+
        ';line-height:'+h+'px;color:#000000;'+this.ftSty+';cursor:default">'+text+'<\/div>';
};


// (Re)draws the GridMap from the data provided in params.
// Event handlers for clicks and tips are set up.
//
// Input:
//
// jg                   the grahics context
//
// params = {
//     width:           width
//     height:          height
//     th:              title height, e.g. 12 (fontsize = th-3)
//     regions:         {regionname: [x, y, w]}     (layout)
//     sites:           {sitename: [x, y, w, h] }   (layout)
//     data:            {sitename: metrics}         (colors)
//     showsitenames:   true/false
//     metric:          function(metrics)      -> value
//     color:           function(value)        -> color
//     regiontip:       function(gmdata, name) -> message
//     sitetip:         function(gmdata, name) -> message
//     regionclick:     function(gmdata, name, rightclick)
//     siteclick:       function(gmdata, name, rightclick)
// }
//
// gmdata               reference to the model (not accessed by this function,
//                      only passed to tip/click functions)
//
function gridmap_generic(jg, params, gmdata)
{
    var regions = params.regions;
    var sites   = params.sites;
    var th      = params.th;
    var data    = params.data;   // { sitename: metrics }
    var metric  = params.metric; // function which extracts the metric value
    var color   = params.color;  // function which maps the metric value to a color

    jg.clear();
    jg.setPrintable(true);
    jg.setFont('verdana', (th-3)+'px', Font.BOLD);  // for titles
    jg.setColor("#888888");
    jg.fillRect(0, 0, params.width, params.height);

    for (var name in regions) {
        if (regions.hasOwnProperty(name)) {
            var r = regions[name];

            jg.setColor("#CCCCCC");
            jg.fillRect1(r[0], r[1]-th+1, r[2]-1, th-2, "region='"+name+"'", name);
        }
    }

    jg.setFont('verdana', '9px', Font.PLAIN);   // for sitenames
    var textheight = 9+1;                       // add 1 for IE

    for (name in sites) {
        if (sites.hasOwnProperty(name)) {
            var r = sites[name];
            var col = '#FFFFFF';                // default if no metrics data available for this site

            if (data.hasOwnProperty(name.toLowerCase())) {
                col = color(metric(data[name.toLowerCase()])); // determine color for metric
            }

            var sitename = (params.showsitenames && r[3]>9 && r[2]>2) ? name : "";

            jg.setColor(col);
            jg.fillRect1(r[0], r[1], r[2], r[3], "site='"+name+"'", sitename);
        }
    }

    jg.setFont('verdana', '9px', Font.ITALIC);
    jg.setColor("#000000");
    jg.drawStringRect("&copy; CERN openlab / EDS", params.width-150, params.height, 150, "right");

    jg.paint();     // creates the DOM objects by setting innerHTML


    // define the handler functions for onmouseover and onclick events
    // (these functions have access to gmdata and params via closure!)
    var regiontip_handler = function() {
        var region = this.getAttribute('region');
        if (region && region!=="") {
            var msg = params.regiontip(gmdata, region);
            Tip(msg||"no info", TITLE, region, DELAY, 0);
        }
    };
    var regionclick_handler = function() {
        var region = this.getAttribute('region');
        if (region && region!=="") {
            params.regionclick(gmdata, region);
        }
    };
    var regionrightclick_handler = function(e) {
        var e = new Event(e).stop();                    // prevents default right click
        var region = this.getAttribute('region');
        if (region && region!=="") {
            params.regionclick(gmdata, region, true);
        }
    };
    var sitetip_handler = function() {
        var site = this.getAttribute('site');
        if (site && site!=="") {
            var msg = params.sitetip(gmdata, site);
            Tip(msg||"no info", TITLE, site, DELAY, 0);
        }
    };
    var siteclick_handler = function() {
        var site = this.getAttribute('site');
        if (site && site!=="") {
            params.siteclick(gmdata, site);
        }
    };
    var siterightclick_handler = function(e) {
        var e = new Event(e).stop();                    // prevents default right click
        var site = this.getAttribute('site');
        if (site && site!=="") {
            params.siteclick(gmdata, site, true);
        }
    };

    // set the onmouseover and onclick event handlers
    if (jg.cnv && jg.cnv.getElementsByTagName) {
        var divs = jg.cnv.getElementsByTagName("div");  // jsgraphics draws in <div> elements
        for (var i = 0; i < divs.length; i++) {
            var region = divs[i].getAttribute('region');
            var site = divs[i].getAttribute('site');
            if (region && region!=="") {
                divs[i].onmouseover = regiontip_handler;
                divs[i].onmouseout = UnTip;
                divs[i].onclick = regionclick_handler;
                divs[i].oncontextmenu = regionrightclick_handler;
            }
            else if (site && site!=="") {
                divs[i].onmouseover = sitetip_handler;
                divs[i].onmouseout = UnTip;
                divs[i].onclick = siteclick_handler;
                divs[i].oncontextmenu = siterightclick_handler;
            }
        }
    }

}


// Draws a color key caption for status metrics
//
// Input:
// jg                   the grahics context
// params = {
//     width:           total width of all color key boxes
//     height:          height of color key boxes (without caption text, total height is 15px larger)
//     space:           horizontal space between color key boxes
//     caption:         list of status values to draw color key rects for, e.g. ["down", "degraded, "ok"]
//     descr:           optional mapping of status values to text strings, e.g. {"down":"Down", "degraded":"Degraded", "ok":"Ok"}
//     color:           function(status) -> color
// }
function gridmap_colorkey_status(jg, params)
{
    var n = params.caption.length;
    var w = (params.width - (n-1)*params.space)/n;

    jg.clear();
    jg.setPrintable(true);
    jg.setFont('verdana', '9px', Font.PLAIN);

    for (var i=0; i<n; i++) {
        var x = i*(w+params.space);
        var x1 = Math.round(x);
        var x2 = Math.round(x+w);
        var status = params.caption[i];

        jg.setColor(params.color(status));
        jg.fillRect(x1, 0, x2-x1, params.height);
        jg.setColor('#000000');
        jg.drawStringRect(params.descr?params.descr[status]:status, x1, params.height+6, x2-x1, "center");
    }

    jg.paint();
}

// Draws color key caption for percentage metrics
//
// Input:
// jg                   the grahics context
// params = {
//     width:           total width of color key box (caption text may need additional space)
//     height:          height of color key box (without caption text, total height is 15px larger)
//     n:               number of different colors to split the interval [0%..100%] into
//     caption:         list of percentage values to draw as caption text
//     color:           function(value) -> color
// }
function gridmap_colorkey_percentage(jg, params)
{
    var n = params.n;

    jg.clear();
    jg.setPrintable(true);
    jg.setFont('verdana', '9px', Font.PLAIN);

    for (var i=0; i<n; i++) {
        var x1 = Math.round(params.width*i/n);
        var x2 = Math.round(params.width*(i+1)/n);

        jg.setColor(params.color(100*i/(n-1)));
        jg.fillRect(x1, 0, x2-x1, params.height);
    }

    jg.setColor('#000000');
    for (i=0; i<params.caption.length; i++) {
        var p = params.caption[i];
        var x = Math.round(params.width*p/100);

        jg.fillRect(x, params.height, 1, 4);
        jg.drawStringRect(p+"%", x-15, params.height+6, 40, "center");
    }

    jg.paint();
}
