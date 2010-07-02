// This file is part of the GridMap software (see http://gridmap.cern.ch)
// Copyright (c) EDS and CERN 2007/2008, patent pending
//
// Author: Max Boehm, max.boehm@eds.com, max.boehm@cern.ch
//
// Contributors:
// Lukasz Kokoszkiewicz [lukasz@kokoszkiewicz.com]
//
// History:
// 18.09.2007  mb        first internal version
// 19.10.2007  mb        1st deployed version, showed at EGEE'07 conference
// 25.11.2007  mb        release v01, complete overwork
// 17.01.2008  mb        continuous availability
// 20.02.2008  mb        release v02
//

// needs:
// - wz_jsgraphics.js     jsGraphics()
// - wz_tooltip_mb.js     Tip(), TITLE, DELAY, STICKY
// - gmdata.js            ajax_mappings()
// - gridmap.js           gridmap_generic()

// helper function:
// returns the time period as a user friendly string
// period               returned string
// "latest"             "20 Nov 2007 14:43 UTC"
// "hour"               "20 Nov 2007 12:00-12:59 UTC"
// "day"                "19 Nov 2007 (whole day)"
// "week"               "12 Nov 2007 (whole week)"
// "month"              "1 Oct 2007 (whole month)"
function timestamp_string(period, ts)
{
    var d = new Date(ts*1000);
    var str = d.toGMTString();
    if (period=="hour") {
        str = str.replace(/(\d\d):(\d\d):(\d\d)/,"$1:00-$1:59");
    }
    else if (period=="latest") {
        str = str.replace(/(\d\d):(\d\d):(\d\d)/,"$1:$2");
    }
    else {
        str = str.replace(/(\d\d):(\d\d):(\d\d).*/,"(whole "+period+")");
    }
    return str.replace(/[a-zA-Z]*, /, "");
}

// helper function:
// rounds ts down to integral of period and adds delta units of period
function timestamp_delta(period, ts, delta)
{
    if (period=="hour") {
        ts = Math.floor(ts/3600+delta)*3600;    // round to hour, add delta
    }
    else if (period=="day") {
        ts = Math.floor(ts/86400+delta)*86400;  // round to day, add delta
    }
    else if (period=="week") {
        ts = (Math.floor((ts/86400+3)/7+delta)*7-3)*86400;  // round to week, add delta
    }
    else if (period=="month") {
        var d = new Date(ts*1000);              // round to month, add delta
        var x = d.getFullYear()*12 + d.getMonth() + delta;
        var y = Math.floor(x/12);
        ts = Date.UTC(y, x-y*12, 1, 0, 0, 0)/1000;
    }
    return ts;
}

// helper: checks if the object obj has properties
function has_properties(obj)
{
    for (var x in obj) {
        if (obj.hasOwnProperty(x)) { return true; }
    }
    return false;
}


// ---------------------


// read in the global mappings required to create the urls to Gridview pages
var _gv_mappings = null;
ajax_mappings(function(obj) { _gv_mappings = obj; });


// add general Gridview parameters to url and invoke link
function open_gridview(url, sitename, vo, period, ts, relFlag, contAvailFlag)
{
    url += "&RelOrAvail=" + (relFlag?"Reliability":"Availability") + "&ContAvailFlag=" + (contAvailFlag?"ON":"OFF");

    sitename = sitename.toLowerCase();
    if (_gv_mappings.sitemap.hasOwnProperty(sitename)) {
        url += "&LTier1Site=" + _gv_mappings.sitemap[sitename] + "&LTier2Site[]=" + _gv_mappings.sitemap[sitename];
    } else {
        return;
    }

    if (_gv_mappings.vomap.hasOwnProperty(vo)) {
        url += "&DefVO=" + _gv_mappings.vomap[vo];
    } else {
        return;
    }

    // map period to Gridview durations
    var gv_period_duration = {"latest":"current", "hour":"current", "day":"hourly", "week":"daily", "month":"daily"};
    var now = new Date().getTime()/1000;
    if ( gv_period_duration[period]=="current" && now - ts > 24*3600 ) {
        period = "day";
    }
    url += "&DurationOption="+gv_period_duration[period];

    // "latest", "hour": set only EndDate
    // "day", "week", "month": set startDate and EndDate
    if (period!="latest" && period!="hour") {
        // set StartDate
        var start = new Date(ts*1000);
        url += "&StartDay="+start.getDate()+"&StartMonth="+(start.getMonth()+1)+"&StartYear="+start.getFullYear();
        if (period=="week" || period=="month") {
            ts = timestamp_delta(period, ts, 1);
            ts = timestamp_delta("day", ts, -1);
        }
    } else {
        url += "&StartDay=-1&StartMonth=-1&StartYear=-1";
    }

    // set EndDate
    var end = new Date(ts*1000);
    url += "&EndDay="+end.getDate()+"&EndMonth="+(end.getMonth()+1)+"&EndYear="+end.getFullYear();

    window.open(url, "gridview").focus();
}

// opens a Gridview page with SAM test results of the node
function open_gridview_testresult(gmdata, sitename, nodename, realserv)
{
    var url = "https://gridview.cern.ch/GRIDVIEW/same_index.php?Information=TestResult&TestVO=-1&TestID=-1&SiteFullName=1";

    nodename = nodename.toLowerCase();
    if (_gv_mappings.nodemap.hasOwnProperty(nodename)) {
        url += "&NodeID=" + _gv_mappings.nodemap[nodename];
    } else {
        return;
    }

    if (_gv_mappings.servicemap.hasOwnProperty(realserv)) {
        url += "&LComponent=" + _gv_mappings.servicemap[realserv];
    } else {
        return;
    }

    // only available for "latest", "hour", "day" ("current" and "hourly" in Gridview)
    var period = gmdata.period;
    if (period=="week" || period=="month") {
        period = "day";
    }

    open_gridview(url, sitename, gmdata.vo, period, gmdata.ts, gmdata.metricName=="reliability", gmdata.metricName!="oldalgo");
}

// opens a Gridview page with detail results of the site
function open_gridview_sitedetail(gmdata, sitename)
{
    var url = "http://gridview.cern.ch/GRIDVIEW/same_index.php?&Information=SiteDetail&TestVO=-1&LComponent=-2&NodeID=-1&TestID=-1&SiteFullName=1";

    open_gridview(url, sitename, gmdata.vo, gmdata.period, gmdata.ts, gmdata.metricName=="reliability", gmdata.metricName!="oldalgo");
}

function open_sam_sensortests(gmdata, sitename, service)
{
    var url = "https://lcg-sam.cern.ch:8443/sam" + (gmdata.topo=="pps"?"-pps":"") + "/sam.py?funct=ShowSensorTests&order=SiteName&setdefs=on";

    url += "&sensors=" + (gmdata.serv!="Site"?gmdata.serv:service);
    if (!gmdata.vo) {
        return;
    }
    url += "&vo=" + gmdata.vo;

    if (gmdata.topo=="regions" || gmdata.topo=="pps") {
        // search for the region sitename belongs to
        for (var regionname in gmdata.layout.topodata) {
            if (gmdata.layout.topodata.hasOwnProperty(regionname)) {
                var l = gmdata.layout.topodata[regionname];
                // check if sitename is part of the region
                for (var i=0; i<l.length; i+=1) {
                    if (l[i]==sitename) {
                        url += "&regions=" + regionname;
                        break;
                    }
                }
            }
        }
    }
    else {  // all regions
        url += "&regions=AsiaPacific&regions=CERN&regions=CentralEurope&regions=France&regions=GermanySwitzerland&regions=Italy&regions=NorthernEurope&regions=OpenScienceGrid&regions=Russia&regions=SouthEasternEurope&regions=SouthWesternEurope&regions=UKI&regions=USATLAS&regions=USCMS&regions=Unknown";
    }

    window.open(url, "sam").focus();
}

function open_sam_history(gmdata, nodename, realserv)
{
    var url = "https://lcg-sam.cern.ch:8443/sam" + (gmdata.topo=="pps"?"-pps":"") + "/sam.py?funct=ShowHistory";

    url += "&sensors=" + (realserv!="Site"?realserv:"CE");
    if (!gmdata.vo) {
        return;
    }
    url += "&vo=" + gmdata.vo;
    url += "&nodename=" + nodename;

    window.open(url, "sam").focus();
}


// ---------------------


// returns color for a status ("na", "ok", "down", "degraded", "partial", "maint")
function color_status(status)
{
    var col = {
        'na':'#EEEEEE',         // light grey
        'ok':'#00FF00',         // green
        'degraded':'#FFAA00',   // orange
        'down':'#FF0000',       // red
        'partial':'#00FFFF',
        //'maint':'#EEEE00'       // yellow
        'maint':'#dddddd'       // grey
    };
    return col[status] || '#FFFFFF';
}

// returns a color function for availability, maintenance, unknown, or reliability metrics
function color_function(gmdata)
{
    // 2 red, 4 orange, 2 green
    var col_avail = ['#ff0000', '#ff6644', '#ff9900', '#ffbb00', '#ffcc33', '#ffdd66', '#88ff88', '#00ff00'];

    // white..yellow
    var col_maint = ['#ffffff', '#ffffdb', '#ffffb6', '#ffff92', '#ffff6d', '#ffff49', '#ffff24', '#ffff00'];

    // white..black
    var col_unknown = ['#ffffff', '#dddddd', '#bbbbbb', '#999999', '#777777', '#555555', '#333333', '#111111'];

    // red..blue
    //var col_rel = ['#ff3030', '#df3e4e', '#bf4b6b', '#9f5989', '#7e67a6', '#5e75c4', '#3e82e1', '#1e90ff'];
    //var col_rel = ['#ff3030', '#ff6060', '#da687b', '#b47095', '#8f78b0', '#6980ca', '#4488e5', '#1e90ff'];
    var col_rel = ['#ff3030', '#ff6464', '#ff9898', '#ffcbcb', '#c7e3ff', '#8fc8ff', '#56acff', '#1e90ff'];

    var index = ({"availability":0, "maintenance":1, "unknown":2, "reliability":3, "oldalgo":0})[gmdata.metricName];
    //var col = ([col_avail, col_maint, col_unknown, col_rel])[index];
    var col = ([col_avail, col_maint, col_unknown, col_avail])[index];

    // return actual color function (has access to col via closure)
    return function(value) {
        if (value<0 || value>100) {
            return '#FFFFFF';
        }
        return col[Math.floor(value*col.length/101)];
   };
}


// ---------------------


// helper: returns css color class for value (-1: "color-na", 0..50%: "color-down", 50..100%: "color-ok")
function av_to_css(value)
{
    if (value<0) { return "color-na"; }
    if (value<50) { return "color-down"; }
    return "color-ok";
}

// helper: returns css color class for status
function status_to_css(status)
{
    if (status.indexOf("maint")>=0) {
        return "color-maint";
    }
    return "color-"+status;
}

// helper: returns "value%" or "na" (if value<0)
function percentage_to_str(value)
{
    return value<0 ? "na" : value+"%";
}

// helper: returns description string for layout metric key ("cpu", "tc", "rj")
function layoutMetric_to_str(gmdata)
{
    var tab = {"cpu":"Total CPUs", "tc":"Total CPUs", "fc":"Free CPUs", "rj":"Running Jobs", "wj":"Waiting Jobs", "tj":"Total Jobs", "do":"Dropouts", "pc":"Physical CPUs", "si":"SPECint2000"};
    var value = tab[gmdata.layoutMetric] || gmdata.layoutMetric;

    if (gmdata.layoutMetric=="tc") {
        if (gmdata.layoutSi2k) {
            value = "Installed Capacity";
        }
        if (gmdata.topo=="tiers") {
            var wlcg_vo = gmdata.vo=='Alice' || gmdata.vo=='Atlas' || gmdata.vo=='CMS' || gmdata.vo=='LHCb';
            value += wlcg_vo?" (WLCG, "+gmdata.vo+")":" (WLCG)";
        } else {
            if (gmdata.layoutVOView)
                value += " ("+gmdata.vo+")";
        }
    }
    return value;
}

// helper: returns description string for metricName
function metricName_to_str(value)
{
    var tab = {"availability":"availability", "reliability":"reliability", "maintenance":"in maintenance", "unknown":"unknown", "oldalgo":"availability (old algorithm)"};
    return tab[value] || value;
}

// helper: returns line or table for layoutMetric "tc" and "rj"
function cpus_si2k_info(gmdata, name)
{
    var m = gmdata.layout.sitedata[name];
    if (!m) {
        return "";
    }
    var tc=0, si=1, pc=2, lc=3;
    if (gmdata.layoutMetric=="tc" && gmdata.layoutStrict) {
        tc=3; lc=0;
    }
    if (has_properties(gmdata.metric.data)) {
        var which = (gmdata.layoutMetric=="tc"&&m[tc]==m[lc] ? 'logical' : (gmdata.layoutMetric=="tc"&&m[tc]==m[pc] ? 'physical' : 'total'));
        var capacity = gmdata.layoutSi2k ? Math.round(m[si]!=-1?m[si]/1000:-1)+" kSI2k" : m[0];

        return layoutMetric_to_str(gmdata) + ": <span class='color-"+which+"'>"+(which!="logical"&&gmdata.layoutMetric=="tc"&&gmdata.layoutSi2k?"~":"")+capacity;
    }
    else {
        var msg = "<table class='tiptable'>";
        if (gmdata.layoutMetric=="tc") {
            msg += "<tr><td></td><td class='smalltext'>Total</td><td class='smalltext'>Physical</td><td class='smalltext'>Logical</td><td></td></tr>";
        }
        msg += "<tr align='left'><th>" + layoutMetric_to_str(gmdata) + ":&nbsp;</th>" +
                  (gmdata.layoutMetric=="tc"&&m[tc]==m[lc] ?
                   "<th></th><th></th><th align='right' class='color-logical'>"+m[lc] :
                   (gmdata.layoutMetric=="tc"&&m[tc]==m[pc] ?
                    "<th></th><th align='right' class='color-physical'>"+m[pc]+"</th><th>" :
                    "<th align='right'>"+m[tc]+"</th><th></th><th>")) +
                  "</th><th>" + (m[si]?"("+Math.round(m[si]/1000)+" kSI2k)":"") + "</th></tr>";
        var nodedict = m[m.length-1];
        for (var node in nodedict) {
            if (nodedict.hasOwnProperty(node)) {
                m = nodedict[node];
                msg += "<tr><td>" + node + ":</td><td align='right'>"+m[tc]+"</td>" +
                       (gmdata.layoutMetric=="tc"&&m[pc]?"<td align='right' class='color-physical'>"+m[pc]:"<td>") +
                       (gmdata.layoutMetric=="tc"&&m[lc]?"<td align='right' class='color-logical'>"+m[lc]:"<td>") +
                       "</td><td>(" + m[si] + " SI2k/Core)</td></tr>";
            }
        }
        msg += "</table>";
        return msg;
    }
}


// HTML for region title tooltip
function regiontip(gmdata, name) {
    var msg = "";
    var tc=0, si=1, pc=2, lc=3;
    if (gmdata.layoutMetric=="tc" && gmdata.layoutStrict) {
        tc=3; lc=0;
    }

    // #CPUs or #RunningJobs of the individual sites
    if (gmdata.layout.topodata.hasOwnProperty(name)) {
        var sitelist = gmdata.layout.topodata[name];

        // metrics[0]: CPU or Jobs, metrics[1]: si2k
        // function to extract size from metrics (-1 means no data available)
        var sizefunc = gmdata.layoutSi2k ? function(m) {return m[si]!=-1?m[si]/1000:-1;} : function(m) {return m[0];} ;
        var unit = gmdata.layoutSi2k ? " kSI2k" : "";

        // sort sitelist
        sitelist.sort(function(a, b) {
            a = gmdata.layout.sitedata.hasOwnProperty(a) ? sizefunc(gmdata.layout.sitedata[a]) : -2;
            b = gmdata.layout.sitedata.hasOwnProperty(b) ? sizefunc(gmdata.layout.sitedata[b]) : -2;
            return b - a;
        });

        var total = 0;
        for (var i=0; i<sitelist.length; i+=1) {
            var sitename = sitelist[i];
            if (gmdata.layout.sitedata.hasOwnProperty(sitename)) {
                var m = gmdata.layout.sitedata[sitename];
                var size = sizefunc(m);
                var which = (gmdata.layoutMetric=="tc"&&m[tc]==m[lc] ? 'logical' : (gmdata.layoutMetric=="tc"&&m[tc]==m[pc] ? 'physical' : 'total'));

                if (size>0) {           // size metric available
                    msg += "<tr><td>" + sitename + ":</td><td align='right' class='color-"+which+"'>" + Math.round(size) + unit + "</td></tr>";
                    total += size;
                } else if (size==-1) {  // size metric is not available
                    msg += "<tr style='color:#880000;'><td>" + sitename + ":</td><td align='right'>no data</td></tr>";
                } else {                // size metric is zero (or negative)
                    msg += "<tr style='color:#FF0000;'><td>" + sitename + ":</td><td align='right'>(not shown) " + Math.round(size) + unit + "</td></tr>";
                }
            }
            else {  // sitename not in sitedata
                msg += "<tr style='color:#0000FF;'><td>" + sitename + ":</td><td align='right'>not in BDII</td></tr>";
            }
        }

        msg = "<table class='tiptable'><tr><th align='left'>" + layoutMetric_to_str(gmdata) + ":&nbsp;</th><th align='right'>" + Math.round(total) + unit + "</th></tr>" + msg + "</table>";
    }
    return msg;
}

// HTML for site status tooltip
function sitetip_sitestatus(gmdata, name, showlinks) {
    var msg = "";
    if (gmdata.metric.data.hasOwnProperty(name.toLowerCase())) {
        var values = gmdata.metric.data[name.toLowerCase()];  // values = [status, m1, m2, m3, ..]

        var timestr = timestamp_string(gmdata.period, gmdata.ts);

        msg += "<table class='tooltiptable' cellpadding='0' cellspacing='0'>";
        msg += "<tr>";
        msg += "<td><span class='"+status_to_css(values[0])+"' style='font-weight:bold;'>overall site status</span></td>";
        msg += "<td class='right'>&nbsp;&nbsp;<span class='"+status_to_css(values[0])+"' style='font-weight:bold;'>" + values[0] + "</span></td>";
        msg += "</tr>";
        msg += "<tr><td colspan='2'><i>"+timestr+"</i></td></tr>";

        for (var i=1; i<gmdata.metric.metricnames.length; i++) {
            if (values[i]) {
                msg += "<tr>";
                if (showlinks) {
                    msg += "<td><a href='javascript:_GM(\""+name+"\",\""+gmdata.metric.metricnames[i]+"\")'><span class='"+status_to_css(values[i])+"'>" + gmdata.metric.metricnames[i] + "</span></a></td>";
                    msg += "<td class='right'>&nbsp;&nbsp;<span class='"+status_to_css(values[i])+"'>" + values[i] + "</span></td>";
                } else {
                    msg += "<td><span class='"+status_to_css(values[i])+"'>" + gmdata.metric.metricnames[i] + "</span></td>";
                    msg += "<td class='right'>&nbsp;&nbsp;<span class='"+status_to_css(values[i])+"'>" + values[i] + "</span></td>";
                }
                msg += "</tr>";
            }
        }
        msg += "</table>";
    }
    else if (has_properties(gmdata.metric.data)) {
        msg = "Site does not support " + gmdata.vo + " VO<br>(no status data available in SAM/GridView)<br>";
    }
    return msg + cpus_si2k_info(gmdata, name);
}

// HTML for site availability tooltip
function sitetip_siteav(gmdata, name) {
    var msg = "";
    if (gmdata.metric.data.hasOwnProperty(name.toLowerCase())) {
        var values = gmdata.metric.data[name.toLowerCase()];      // [av, av1, av2, av3, ...]

        msg += "<table class='tooltiptable' cellpadding='0' cellspacing='0'>";
        msg += "<tr>";
        msg += "<td><span class='"+av_to_css(values[0])+"' style='font-weight:bold;'>"+metricName_to_str(gmdata.metricName)+" status</span></td>";
        msg += "<td class='right'>&nbsp;&nbsp;<span class='"+av_to_css(values[0])+"' style='font-weight:bold;'>" + percentage_to_str(values[0]) + "</span></td>";
        msg += "</tr>";
        msg += "<tr><td colspan='2'><i>"+timestamp_string(gmdata.period, gmdata.ts)+"</i></td></tr>";

        for (var i=1; i<gmdata.metric.metricnames.length; i++) {
            if (values[i]>=0) {
                msg += "<tr>";
                msg += "<td><span class='"+av_to_css(values[i])+"'>" + gmdata.metric.metricnames[i] + "</span></td>";
                msg += "<td class='right'>&nbsp;&nbsp;<span class='"+av_to_css(values[i])+"'>" + percentage_to_str(values[i]) + "</span></td>";
                msg += "</tr>";
            }
        }
        msg += "</table>";
    }
    else if (has_properties(gmdata.metric.data)) {
        msg = "Site does not support " + gmdata.vo + " VO<br>(no availability data available in SAM/GridView)<br>";
    }
    return msg + cpus_si2k_info(gmdata, name);
}

// HTML for site service status tooltip
function sitetip_siteserstatus(gmdata, name, showlinks) {
    var msg = "";
    if (gmdata.metric.data.hasOwnProperty(name.toLowerCase())) {
        var values = gmdata.metric.data[name.toLowerCase()];      // [status, {node: status}]

        for (serv in values[1]) {
            var nodestatus = values[1][serv][1];

            msg += "<table class='tooltiptable' cellpadding='0' cellspacing='0'>";
            msg += "<tr>";
            msg += "<td><span class='"+status_to_css(values[1][serv][0])+"' style='font-weight:bold;'>overall " + serv + " status</span></td>";
            msg += "<td class='right'>&nbsp;&nbsp;<span class='"+status_to_css(values[1][serv][0])+"' style='font-weight:bold;'>" + values[1][serv][0] + "</span></td>";
            msg += "</tr>";
            msg += "<tr><td colspan='2'><i>"+timestamp_string(gmdata.period, gmdata.ts)+"</i></td></tr>";

            for (var node in nodestatus) {
                if (nodestatus.hasOwnProperty(node)) {
                    msg += "<tr>";
                    if (showlinks) {
                        msg += "<td><a href='javascript:_GM(\""+name+"\",\""+node+"\", \""+serv+"\")'><span class='"+status_to_css(nodestatus[node])+"'>" + node + "</span></a></td>";
                        msg += "<td class='right'>&nbsp;&nbsp;<span class='"+status_to_css(nodestatus[node])+"'>" + nodestatus[node] + "</span></td>";
                    } else {
                        msg += "<td><span class='"+status_to_css(nodestatus[node])+"'>" + node + "</span></td>";
                        msg += "<td class='right'>&nbsp;&nbsp;<span class='"+status_to_css(nodestatus[node])+"'>" + nodestatus[node] + "</span></td>";
                    }
                    msg += "</tr>";
                }
            }
            msg += "</table>";
        }
    }
    else if (has_properties(gmdata.metric.data)) {
        // in case of "serv1-serv2-serv3" show "serv1" only
        msg = "Site does not support " + gmdata.serv.replace(/-.*/,"") + " service for " + gmdata.vo +
              " VO<br>(no status data available in SAM/GridView)<br>";
    }
    return msg + cpus_si2k_info(gmdata, name);
}

// HTML for site service availability tooltip
function sitetip_siteserav(gmdata, name, showlinks) {
    var msg = "";
    if (gmdata.metric.data.hasOwnProperty(name.toLowerCase())) {
        var values = gmdata.metric.data[name.toLowerCase()];      // [av, {node: av}]

        for (serv in values[1]) {
            var nodeav = values[1][serv][1];

            msg += "<table class='tooltiptable' cellpadding='0' cellspacing='0'>";
            msg += "<tr>";
            msg += "<td><span class='"+av_to_css(values[1][serv][0])+"' style='font-weight:bold;'>overall " + serv + " " + metricName_to_str(gmdata.metricName) + "</span></td>";
            msg += "<td class='right'>&nbsp;&nbsp;<span class='"+av_to_css(values[1][serv][0])+"' style='font-weight:bold;'>" + percentage_to_str(values[1][serv][0]) + "</span></td>";
            msg += "</tr>";
            msg += "<tr><td colspan='2'><i>"+timestamp_string(gmdata.period, gmdata.ts)+"</i></td></tr>";

            for (var node in nodeav) {
                if (nodeav.hasOwnProperty(node)) {
                    msg += "<tr>";
                    if (showlinks) {
                        msg += "<td><a href='javascript:_GM(\""+name+"\",\""+node+"\", \""+serv+"\")'><span class='" + av_to_css(nodeav[node]) + "'>" + node + "</span></a></td>";
                        msg += "<td class='right'>&nbsp;&nbsp;<span class='"+av_to_css(nodeav[node])+"'>" + percentage_to_str(nodeav[node]) + "</span></td>";
                    } else {
                        msg += "<td><span class='" + av_to_css(nodeav[node]) + "'>" + node + "</span></td>";
                        msg += "<td class='right'>&nbsp;&nbsp;<span class='"+av_to_css(nodeav[node])+"'>" + percentage_to_str(nodeav[node]) + "</span></td>";
                    }
                    msg += "</tr>";
                }
            }
            msg += "</table>";
        }
    }
    else if (has_properties(gmdata.metric.data)) {
        msg = "Site does not support " + gmdata.serv.replace(/-.*/,"") + " service for " + gmdata.vo + " VO<br>(no availability data available in SAM/GridView)<br>";
    }
    return msg + cpus_si2k_info(gmdata, name);
}


// ---------------------


// Global reference to the handler function which is invoked when the user clicks on a link in a tooltip.
// The tooltip can e.g. contain HTML code like the following: "<a href='javascript:_GM(...)'>...</a>"
var _GM = null;


// Custom GridMap view class
//
// - canvas  the name (id) or reference of the <div> element of the gridmap.
//           For example "gridmapCanvas" when the div element is
//           <div id="gridmapCanvas" style="position:relative;width:800px;height:600px"></div>
//
// the constructor creates the graphics object to draw into
function GMView(canvas)
{
    // public members
    this.jg = new jsGraphics(canvas);   // canvas is the name or the element itself

    // updates the gridmap view based on gmdata
    this.update = function(gmdata)
    {
        if (gmdata.layout && gmdata.metric) {
            var sitetip;
            var isstatus = gmdata.period=="latest";
            if (isstatus) {
                sitetip = (gmdata.serv=="Site"?sitetip_sitestatus:sitetip_siteserstatus);
            } else {
                sitetip = (gmdata.serv=="Site"?sitetip_siteav:sitetip_siteserav);
            }

            // Define the function which is called when the user clicks on a site. It shows
            // the current sitetip as a sticky tooltip with clickable links.
            // (this function knows the sitetip via closure!)
            var siteclick = function siteclick(gmdata, name, rightclick) {
                var msg;
                // set the global handler function _GM which is invoked from "<a href='javascript:_GM(..)'>..</a>"
                // when the user clicks on a link in a tooltip (function has access to gmdata via closure!)
                _GM = function(sitename, param2, realserv) {
                    if (gmdata.serv=="Site") {
                        // param2 is servicename
                        open_sam_sensortests(gmdata, sitename, param2);
                    } else {
                        // param2 is nodename
                        if (gmdata.period=="latest") {
                            open_sam_history(gmdata, param2, realserv);
                        } else {
                            open_gridview_testresult(gmdata, sitename, param2, realserv);
                        }
                    }
                };
                if (rightclick) {
                    msg = sitetip(gmdata, name, true);
                    Tip(msg, TITLE, name, DELAY, 0, STICKY, true, OFFSETX, -10, OFFSETY, -10);
                } else {
                    if (gmdata.serv=="Site") {
                        if (gmdata.period=="latest") {
                            msg = sitetip(gmdata, name, true);
                            Tip(msg, TITLE, name, DELAY, 0, STICKY, true);
                        } else {
                            open_gridview_sitedetail(gmdata, name);
                        }
                    } else {
                        msg = sitetip(gmdata, name, true);
                        Tip(msg, TITLE, name, DELAY, 0, STICKY, true);
                    }
                }
            };

            // call generic gridmap drawing function
            gridmap_generic(this.jg, {
                width:          (gmdata.layout.size&&gmdata.layout.size.width)||gmdata.width,
                height:         (gmdata.layout.size&&gmdata.layout.size.height)||gmdata.height,
                th:             gmdata.th,
                regions:        gmdata.layout.regions,
                sites:          gmdata.layout.sites,
                data:           gmdata.metric.data,
                showsitenames:  gmdata.showsitenames,

                metric:         function(metrics) { return metrics[0]; },
                color:          isstatus?color_status:color_function(gmdata),
                regiontip:      regiontip,
                sitetip:        sitetip,
                regionclick:    function(gmdata, name, rightclick) {
                                    if (!rightclick) {
                                        gmdata.setTopo(gmdata.topo, gmdata.topoDrillDown && gmdata.topo!="all"?"":name);
                                        gmdata.updateGridmap();
                                    } else {
                                        var msg = regiontip(gmdata, name);
                                        Tip(msg, TITLE, name, DELAY, 0, STICKY, true, OFFSETX, -10, OFFSETY, -10);
                                    }
                                },
                siteclick:      siteclick
            }, gmdata);
        }
    };
}
