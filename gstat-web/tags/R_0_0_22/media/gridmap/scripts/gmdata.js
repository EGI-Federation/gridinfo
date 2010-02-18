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
// 25.11.2007  mb        release v01, cleanup
// 17.01.2008  mb        continuous availability
// 20.02.2008  mb        release v02
// 21.01.2009  lk        Dynamic service drop down list, OSG checkbox
// 23.02.2009  mb        logical CPUs by default, MoU checkbox
// 20.03.2009  lk        allwlcg checkbox
//

// needs:
// - gmview.js          update(), timestamp_delta(), timestamp_string()
// - mootools.js        periodical(), Ajax, Json
// - cache.js           in ajax_* functions

// Gridmap data class (model)
//
// Manages the data required to draw the gridmap.
// Interacts with the server via Ajax calls.
// The Ajax calls use the global cache object _gm_cache.
//
// constructor takes:
// - gmview     the attached view object
// - w, h       the size of the view
function GMData(gmview, width, height)
{
    this.gmview = gmview;   // reference to the gridmap view object

    // layout parameters (size of rects)
    this.width = width;
    this.height = height;
    this.th = 12;       // title height, e.g. 12 (fontsize = th-3)
    this.layoutMetric;  // "cpu", "tc", "fc", "rj", "wj", "tj"
    this.layoutUseHist; // if true, historical gstat cpu numbers will be used
    this.layoutVOView;  // true if vo specific data shall be used for the layout
                        // (then changing the vo will also make the layout dirty!)
    this.layoutSi2k;    // if true, SPECint2000 values will be shown instead of number of CPUs
    this.layoutStrict;  // if true, only logical CPU numbers will be used (no fallback logic)
    this.topo;          // name of topology view, e.g. "regions", "tiers", "pps", "all", ...
    this.topoDrillDown; // "" or regionname to drill down
    this.showsitenames; // show sitenames in rectangles
    this.showosgsites;  // show OSG sites
    this.allwlcg;       // in the "tiers" view show all WLCG sites (not only of the selected VO)

    // associated layout data (retrieved via Ajax or from cache)
    this.layout;
    this.layoutDirty;

    // metric parameters (colors of rects)
    this.vo;
    this.serv;
    this.period;        // latest, hour, day, week, month
    this.ts = 0;        // must initially have some numeric value
    this.tsCallback;    // function to call when timestamp is updated

    this.metricName;    // "availability", "reliability", "maintenance", "unknown", "oldalgo"

    // associated metric data (retrieved via Ajax or from cache)
    this.metric;
    this.metricDirty;

    // this flag is used to indicate that the view needs an update, but no
    // new data needs to be retrieved via Ajax.
    // (needs not to be set if layoutDirty or metricDirty are already set)
    this.viewDirty;

    // reference to the last active Ajax call for layout and metric (mootools)
    this.ajaxLayout = null;
    this.ajaxMetric = null;

    // callback
    this.updateCallback;// function to call after view has been updated

    this.intervalTimer = null;  // this is used for automatic updates if period="latest"


    // helper: sets the view dirty and cancels a pending ajax call
    this.setLayoutDirty = function() {
        this.layoutDirty = true;
        if (this.ajaxLayout) { this.ajaxLayout.cancel(); this.ajaxLayout = null; }
    };

    this.setMetricDirty = function() {
        this.metricDirty = true;
        if (this.ajaxMetric) { this.ajaxMetric.cancel(); this.ajaxMetric = null; }
    };

    this.setSize = function(width, height) {
        this.width = width;
        this.height = height;
        this.setLayoutDirty();
    };

    // select layout metric "cpu", "tc", "rj"
    this.setLayoutMetric = function(layoutMetric) {
        this.layoutMetric = layoutMetric;
        this.setLayoutDirty();

        if (layoutMetric=="cpu") {  // use GStat CPU numbers
            // voview and si2k only available from bdii, osg sites are not contained in GStat
            this.layoutVOView = false;
            this.layoutSi2k = false;
            this.showosgsites = false;
        } else {                    // use BDII data (CPUs or running Jobs)
            // historical cpu numbers only available from gstat
            this.layoutUseHist = false;
        }
    };

    // select if the layout shall use historical CPU numbers from gstat (true/false)
    this.setLayoutUseHist = function(layoutUseHist) {
        this.layoutUseHist = layoutUseHist;
        this.setLayoutDirty();
    };

    // select if the layout shall depend on the VO (true/false)
    this.setLayoutVOView = function(layoutVOView) {
        this.layoutVOView = layoutVOView;
        this.setLayoutDirty();
    };

    // select if the layout shall use SPECint2000 instead of CPU numbers (true/false)
    this.setLayoutSi2k = function(layoutSi2k) {
        this.layoutSi2k = layoutSi2k;
        this.setLayoutDirty();
    };

    // select if the layout shall strictly use logical CPU numbers (true/false)
    this.setLayoutStrict = function(layoutStrict) {
        this.layoutStrict = layoutStrict;
        this.setLayoutDirty();
    };

    // select topology, optionally drill down
    this.setTopo = function(topo, drillDown) {
        var oldTopo = this.topo;
        this.topo = topo;
        this.topoDrillDown = drillDown||"";
        if (topo=="tiers" && this.layoutMetric=="cpu") {    // "tiers" view needs BDII data source
            this.setLayoutMetric("tc");
        }
        this.setLayoutDirty();
        if ((oldTopo == "pps" && topo != "pps") || (topo == "pps" && oldTopo != "pps")) {
            this.setMetricDirty();
        }
        if (topo!="tiers") {
            this.allwlcg = false;   // reset allwlcg
        }
    };

    this.setShowSitenames = function(showsitenames) {
        this.showsitenames = showsitenames;
        this.viewDirty = true;
    };

    this.setShowOsgSites = function(showosgsites) {
        if (this.layoutMetric == 'cpu' && showosgsites) {
            this.setLayoutMetric('tc');
        }
        this.showosgsites = showosgsites;
        this.setLayoutDirty();
    };

    this.setAllWlcg = function(allwlcg) {
        this.allwlcg = allwlcg;
        this.setLayoutDirty();
    };

    this.setVo = function(vo) {
        this.vo = vo;
        this.setMetricDirty();
        
        var topo = this.topo=="tiers";
        var vos = {"Atlas":true,"Alice":true,"CMS":true,"LHCb":true};

        if (!vos[vo] && topo) {
            this.allwlcg = false;   // reset allwlcg
        }
        
        if (this.layoutVOView || topo) {
            this.setLayoutDirty();
        }
    };

    // "Site", "CE", "SE", "SRM", "sBDII", "ArcCE"
    this.setServ = function(serv) {
        this.serv = serv;
        this.setMetricDirty();
    };

    // "latest", "hour", "day", "week", "month"
    // adjust timestamp
    this.setPeriod = function(period) {
        this.period = period;
        this.setMetricDirty();

        // automatically refresh every 5 minutes if period="latest" (use mootools functionality)
        $clear(this.intervalTimer);
        this.intervalTimer = null;
        if (this.period=="latest") {
            this.intervalTimer = this.updateGridmap.periodical(5*60*1000, this, true);
            this.metricName = "availability";       // reset to default
        }

        this.adjustTimestamp(0);
    };

    // set the function to call when the timestamp changes
    this.setTimestampCallback = function(f) {
        this.tsCallback = f;
    };

    // set and adjust timestamp, returns timestamp
    this.setTimestamp = function(ts) {
        this.adjustTimestamp(0, ts);
    };

    // adjust timestamp to start of hour/day/week/month and add delta
    // If set_ts is not null, it is used instead of this.ts
    // calls timestamp callback function
    this.adjustTimestamp = function(delta, set_ts) {
        var oldts = this.ts;

        this.ts = timestamp_delta(this.period, set_ts||this.ts, delta);

        if (oldts!=this.ts) {
            this.setMetricDirty();
        }

        if (this.layoutUseHist && Math.floor(oldts/86400)!=Math.floor(this.ts/86400)) {
            this.setLayoutDirty();
        }

        if (this.tsCallback) { this.tsCallback(timestamp_string(this.period, this.ts)); }
    };

    // "availability" "maintenance", "unknown", "reliability", "oldalgo"
    this.setMetricName = function(metricName) {
        this.metricName = metricName;
        this.setMetricDirty();
    };

    // update layout data for [w, h, topo, topoDrillDown] via Ajax or from cache
    // afterwards call f() on success and e() on error
    this.updateLayout = function(f, e)
    {
        var thisRef = this;     // save reference to "this" to have it available in function

        if (this.layoutMetric=="cpu") {
            // use gstat data
            this.ajax_treemap(this.topo, this.topoDrillDown, this.layoutUseHist?this.ts:"", this.width, this.height, this.th, function(obj) {
                // remember current layout data {sites, regions}
                thisRef.layout = obj;
                thisRef.layoutDirty = false;
                f();
            }, e);
        }
        else {
            // use bdii data
            var lm = (this.layoutMetric=="tc" && this.layoutStrict ? "lc" : this.layoutMetric);
            this.ajax_treemap(this.topo, this.topoDrillDown, this.vo, this.layoutVOView, lm+(this.layoutSi2k?"si":""), this.width, this.height, this.th, this.showosgsites, this.allwlcg, function(obj) {
                // remember current layout data {sites, regions}
                thisRef.layout = obj;
                thisRef.layoutDirty = false;
                f();
            }, e);
        }
    };

    // update metric data for [vo, serv, period, ts] via Ajax or from cache
    // note: if this.period=="latest", this call can make the layout dirty!
    // afterwards call f() on success and e() on error
    this.updateMetric = function(f, e)
    {
        var thisRef = this;     // save reference to "this" to have it available in g()
        var pps = false;

        // function to call when data has been retrieved via Ajax or from cache
        var g = function(obj) {
            // remember current metric data
            thisRef.metric = obj;

            // change sitenames in obj.data dict to lower case
            data1 = {};
            for (var sitename in obj.data) {
                data1[sitename.toLowerCase()] = obj.data[sitename];
            }
            thisRef.metric.data = data1;

            thisRef.metricDirty = false;
            f();
        };

        pps = (this.topo=="pps");

        if (this.serv=="Site") {
            if (this.period=="latest") {
                this.ajax_sitestatuslatest(this.vo, pps, function(obj) {thisRef.setTimestamp(obj.ts); g(obj);}, e);
            } else if (this.metricName=="oldalgo" || this.ts<Date.UTC(2007, 10-1, 1)/1000) {  // use old algorithm before 1 Oct 2007
                this.ajax_siteav(this.vo, this.ts, this.period, pps, g, e);
            } else {
                this.ajax_contsiteav(this.vo, this.ts, this.period, this.metricName, pps, g, e);
            }
        }
        else {
            if (this.period=="latest") {
                this.ajax_siteserstatuslatest(this.vo, this.serv, pps, function(obj) {thisRef.setTimestamp(obj.ts); g(obj);}, e);
            } else if (this.metricName=="oldalgo" || this.ts<Date.UTC(2007, 10-1, 1)/1000) {  // use old algorithm before 1 Oct 2007
                this.ajax_siteserav(this.vo, this.serv, this.ts, this.period, pps, g, e);
            } else {
                this.ajax_contsiteserav(this.vo, this.serv, this.ts, this.period, this.metricName, pps, g, e);
            }
        }
    };

    // set the function to call when view has been updated
    this.setUpdateCallback = function(f) {
        this.updateCallback = f;
    };

    // updates underlaying data via Ajax or from cache if needed
    // afterwards and redraw gridmap if needed
    // if forceRefresh==true new metric data is always retrieved and new layout data
    // is retrieved if it is dynamic BDII data
    this.updateGridmap = function(forceRefresh)
    {
        var thisRef = this;     // save reference to "this" to have it available in draw()

        if (forceRefresh) {
            this.setMetricDirty();        // timed invocation -> update metric
            this.automaticRefresh = true;
        } else {
            this.preventErrorMessages = false; // not a timed invocation -> don't prevent error messages
        }

        if (this.metricDirty && this.layoutMetric=="rj") {
            this.setLayoutDirty();    // refresh layout if it is dynamic BDII data
        }

        // function to call when Ajax call doesn't succeed
        var error = function(transport) {
            if (!thisRef.preventErrorMessages) {
                thisRef.preventErrorMessages = true;   // prevent displaying further error messages

                // invalidate metric and clear view
                thisRef.metric = {data:{}, metricnames:[]};
                gmview.update(thisRef);
                $('gridmapCanvasLoading').setStyle('display', 'none');

                $clear(thisRef.intervalTimer);      // stop interval timer while the error message is displayed
                thisRef.intervalTimer = null;
                alert(transport.responseText);      // show error message
                thisRef.setPeriod(thisRef.period);  // restart interval timer if needed
            }
        };

        // function to call when Ajax call succeeds
        var draw = function() {
            if (!thisRef.layoutDirty && !thisRef.metricDirty) {
                gmview.update(thisRef);
                this.viewDirty = false;
                if (thisRef.updateCallback) { thisRef.updateCallback(thisRef); }
                thisRef.preventErrorMessages = false;  // don't prevent error messages
            }
            else {
                // if period=="latest" do postponed updateLayout() call if needed
                if ((thisRef.period=="latest"&&thisRef.layoutUseHist) && thisRef.layoutDirty) {
                    thisRef.updateLayout(draw, error);
                }
            }
        };

        // is the data up to date but the view needs to be updated?
        if (!this.layoutDirty && !this.metricDirty && this.viewDirty) {
            draw();
            return;
        }

        // layout data or metric data is dirty and needs to be updated via Ajax

        // if period=="latest" the layout may change due to a new timestamp from the new metric data
        // therefore we have to postpone the updateLayout() call in this case
        if (!(this.metricDirty&&this.period=="latest"&&this.layoutUseHist) && this.layoutDirty) {
            this.updateLayout(draw, error);
        }
        if (this.metricDirty) {
            this.updateMetric(draw, error);
        }
    };


    // Functions to retrieve data via Ajax or from cache

    this.wait = function() {
        $('caption').addClass('loading');
        if (!this.automaticRefresh) {
            $('gridmapCanvasLoading').setStyle('display', 'block');
        }
        this.automaticRefresh = false;
    };

    // - topo       topology
    // - drillDown  regionname to drill down or null/empty string
    // - ts         timestamp (only the day,month,year are used)
    // - f          function to call with the data if successfull
    // - e          function to call with if an error occured
    this.ajax_treemap = function(topo, drillDown, ts, width, height, th, f, e) {
        drillDown = drillDown || "";
        if (ts) {
            ts = Math.floor(ts/86400)*86400;
        }
        var key = "treemap_"+topo+"_"+drillDown+"_"+ts+"_"+width+"_"+height+"_"+th;    // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxLayout) { this.ajaxLayout.cancel(); }      // cancel previous ajax request

        this.wait();
        this.ajaxLayout = new Ajax('treemap', {
            method: 'get',
            data: {topo: topo, drillDown:drillDown, ts:ts, width:width, height:height, th:th},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_treemap = function(topo, drillDown, vo, voview, metric, width, height, th, osg, allwlcg, f, e) {
        vo = vo || "";
        drillDown = drillDown || "";
        var key = "treemap_"+topo+"_"+drillDown+"_"+vo+"_"+voview+"_"+metric+"_"+width+"_"+height+"_"+th+"_"+osg+"_"+allwlcg;    // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxLayout) { this.ajaxLayout.cancel(); }

        this.wait();
        this.ajaxLayout = new Ajax('treemap', {
            method: 'get',
            data: {topo:topo, drillDown: drillDown, vo:vo, voview:voview, metric:metric, width:width, height:height, th:th, osg:osg, allwlcg:allwlcg},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_sitestatuslatest = function(vo, pps, f, e) {
        var key = "sitestatuslatest_"+vo+"_"+pps;   // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxMetric) { this.ajaxMetric.cancel(); }

        this.wait();
        this.ajaxMetric = new Ajax('statuslatest', {
            method: 'get',
            data: {vo:vo, pps:pps},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_siteserstatuslatest = function(vo, serv, pps, f, e) {
        var key = "siteserstatuslatest_"+vo+"_"+serv+"_"+pps;   // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxMetric) { this.ajaxMetric.cancel(); }

        this.wait();
        this.ajaxMetric = new Ajax('serstatuslatest', {
            method: 'get',
            data: {vo:vo, serv:serv, pps:pps},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_siteav = function(vo, ts, period, pps, f, e) {
        var key = "siteav_"+vo+"_"+ts+"_"+period+"_"+pps;   // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxMetric) { this.ajaxMetric.cancel(); }

        this.wait();
        this.ajaxMetric = new Ajax('av', {
            method: 'get',
            data: {vo:vo, ts:ts, period:period, pps:pps},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_siteserav = function(vo, serv, ts, period, pps, f, e) {
        var key = "siteserav_"+vo+"_"+serv+"_"+ts+"_"+period+"_"+pps;   // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxMetric) { this.ajaxMetric.cancel(); }

        this.wait();
        this.ajaxMetric = new Ajax('serav', {
            method: 'get',
            data: {vo:vo, serv:serv, ts:ts, period:period, pps:pps},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_contsiteav = function(vo, ts, period, name, pps, f, e) {
        var key = "contsiteav_"+vo+"_"+ts+"_"+period+"_"+name+"_"+pps;   // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxMetric) { this.ajaxMetric.cancel(); }

        this.wait();
        this.ajaxMetric = new Ajax('cav', {
            method: 'get',
            data: {vo:vo, ts:ts, period:period, name:name, pps:pps},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };

    this.ajax_contsiteserav = function(vo, serv, ts, period, name, pps, f, e) {
        var key = "contsiteserav_"+vo+"_"+serv+"_"+ts+"_"+period+"_"+name+"_"+pps;   // unique key for the cache

        var obj = _gm_cache.get(key);
        if (obj) { f(obj); return; }

        if (this.ajaxMetric) { this.ajaxMetric.cancel(); }

        this.wait();
        this.ajaxMetric = new Ajax('cserav', {
            method: 'get',
            data: {vo:vo, serv:serv, ts:ts, period:period, name:name, pps:pps},
            onComplete: function(response) {
                var obj = Json.evaluate(response);
                _gm_cache.add(key, obj, _gm_cache_client_timeout);
                f(obj);
            },
            onFailure: e
        }).request();
    };
}


// ---------------------


function ajax_mappings(f) {
    var ajax = new Ajax('mappings', {
        method: 'get',
        onComplete: function(response) { f(Json.evaluate(response)); },
        onFailure: function(transport) { alert(transport.responseText); }
    }).request();
}

function ajax_samservices(f) {
    var ajax = new Ajax('samservices', {
        method: 'get',
        onComplete: function(response) { f(Json.evaluate(response)); },
        onFailure: function(transport) { alert(transport.responseText); }
    }).request();
}
