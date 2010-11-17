// This file is part of the GridMap software (see http://gridmap.cern.ch)
// Copyright (c) EDS and CERN 2007/2008, patent pending
//
// Author: Max Boehm, max.boehm@eds.com, max.boehm@cern.ch
//
// Contributors:
// Lukasz Kokoszkiewicz [lukasz@kokoszkiewicz.com]
//
// History:
// 25.11.2007  mb        release v01, created
// 17.01.2008  mb        continuous availability
// 20.02.2008  mb        release v02
// 09.09.2008  mb        highlight selected buttons in Safari, Opera
// 21.01.2009  lk        Dynamic service drop down list, OSG checkbox
// 20.02.2009  lk        New bookmarking/history system
// 23.02.2009  mb        updated drawServOptions, updateServUI, history logic, removed "status"
// 19.03.2009  mb        strict checkbox
// 20.03.2009  lk        allwlcg checkbox
//

// needs:
// - mootools.v1.11.js          $(), $$(), $each()
// - gmdata.js
// - cache.js

// UI controller, updates the model gmdata (and thereby indirectly the view attached to gmdata)
function GMControl(gmdata, colorkey)
{
    // ------------------------------
    // Event handler functions

    // event handler for topology selection
    this.selectTopo = function(elem)
    {
        if ($(elem).id=="showsitenames") {
            gmdata.setShowSitenames($(elem).checked);
        }
        else if ($(elem).id=="showosgsites") {
            gmdata.setShowOsgSites($(elem).checked);
            this.updateLayoutMetricUI();
        } else if ($(elem).id=="allwlcg") {
            gmdata.setAllWlcg($(elem).checked);
        } else {
            gmdata.setTopo($(elem).id, "");    // no drilldown
        }

        this.updateLayoutMetricUI();
        this.updateTopoUI();
        gmdata.updateGridmap();
    };

    // event handler for layout metric selection
    this.selectLayoutMetric = function(elem)
    {
        if ($(elem).id=="usehist") {
            gmdata.setLayoutUseHist($(elem).checked);
        } else if ($(elem).id=="usevoview") {
            gmdata.setLayoutVOView($(elem).checked);
        } else if ($(elem).id=="si2k") {
            gmdata.setLayoutSi2k($(elem).checked);
        } else if ($(elem).id=="strict") {
            gmdata.setLayoutStrict($(elem).checked);
        } else {
            gmdata.setLayoutMetric($(elem).id);
        }
        this.updateLayoutMetricUI();
        this.updateTopoUI();
        gmdata.updateGridmap();
    };

    // event handler for VO selection
    this.selectVo = function(elem)
    {
        gmdata.setVo($(elem).value);
        this.updateVoUI();
        this.updateTopoUI(); // for showing/hiding allwlcg checkbox
        gmdata.updateGridmap();
    };

    // event handler for service selection
    this.selectServ = function(elem)
    {
        gmdata.setServ($(elem).id=="serv-select" ? $(elem).value : $(elem).id);
        this.updateServUI();
        gmdata.updateGridmap();
    };

    // event handler for time period selection
    this.selectPeriod = function(elem)
    {
        var previousPeriod = gmdata.period;
        gmdata.setPeriod($(elem).id);

        // if switching from latest -> hour/day/week/month, go back one unit
        gmdata.adjustTimestamp(previousPeriod=="latest" && gmdata.period!="latest" ? -1 : 0);
        this.updatePeriodUI();
        gmdata.updateGridmap();
    };

    // event handler for period-up/period-down buttons
    this.periodUpDown = function(delta)
    {
        if (gmdata.period=="latest" && delta<0) {
            this.selectPeriod($("hour"));
            return;
        }
        gmdata.adjustTimestamp(delta);
        gmdata.updateGridmap();
    };

    // event handler to select Reliability/Maintenance/Unknown/OldAlgorithm
    this.selectMetric = function(elem)
    {
        gmdata.setMetricName($(elem).checked ? $(elem).id : "availability");
        this.updatePeriodUI();
        gmdata.updateGridmap();
    };


    // ------------------------------
    // Functions update UI state to match current settings

    this.drawServOptions = function(services) {
        var servlength = services.length;
        var selectElement = $("serv-select");

        var option = new Element("option", {"value": "Site"});
        option.setText("more...");
        option.injectInside(selectElement);

        for (var i=0; i<servlength; i++) {
            var serv = services[i];
            option = new Element('option', {'value': serv});
            option.setText(serv);
            option.injectInside(selectElement);
        }
    };

    // update topology UI state (topogroup buttons, showsitenames)
    this.updateTopoUI = function()
    {
        $$("#topogroup input").removeClass("bold");
        $$([gmdata.topo]).addClass("bold");

        var tiers = gmdata.topo=="tiers";
        var countries = gmdata.topo=="countries";
        $('showsitenames').checked = gmdata.showsitenames;
        $('showosgsites').disabled = tiers || countries;
        $('showosgsites').checked = gmdata.showosgsites||tiers||countries;

        var wlcg_vo = gmdata.vo=='Alice' || gmdata.vo=='Atlas' || gmdata.vo=='CMS' || gmdata.vo=='LHCb';
        if (tiers && wlcg_vo) {
            $('allwlcg_span').removeClass("hidden");
        } else {
            $('allwlcg_span').addClass("hidden");
        }
        $('allwlcg').disabled = (!tiers || !wlcg_vo);
        $('allwlcg').checked = gmdata.allwlcg;
        $('cpu').disabled = tiers;
    };

    // update layout metric UI state (layoutgroup buttons, usehist, usevoview)
    this.updateLayoutMetricUI = function()
    {
        $$("#layoutgroup input").removeClass("bold");
        $(gmdata.layoutMetric).addClass("bold");

        var cpugstat = gmdata.layoutMetric=="cpu";
        $("usehist").disabled = !cpugstat;
        $("usehist").checked = gmdata.layoutUseHist;
        $("usevoview").disabled = cpugstat;
        $("usevoview").checked = gmdata.layoutVOView;
        $("si2k").disabled = cpugstat;
        $("si2k").checked = gmdata.layoutSi2k;
        $("strict").disabled = cpugstat;
        $("strict").checked = gmdata.layoutStrict;
        if (gmdata.layoutStrict) {
            $$('span[id=more]').removeClass('hidden');
        }
    };

    // update VO UI state (vogroup buttons and text field)
    this.updateVoUI = function()
    {
        // make selected VO bold
        $$("#vogroup input").removeClass("bold");
        if (gmdata.vo) {
            var elems = $$("#vogroup input[value="+gmdata.vo+"]");
            elems.addClass("bold");
            if (!elems.length) {          // custom vo
                $("vo").value = gmdata.vo;
                $("vo").addClass("bold");
            }
        }
    };

    // update service UI state (servgroup buttons and text field)
    this.updateServUI = function()
    {
        // define select element
        var servSelect = $('serv-select');

        // make selected service bold
        $$("#servgroup input").removeClass("bold");
        if (gmdata.serv) {
            var elems = $$("#servgroup input[id="+gmdata.serv+"]");
            elems.addClass("bold");

            if (elems.length) {
                servSelect.selectedIndex = 0;
            }

            // make selected services options bold
            var services = gmdata.serv.split("-");
            if (gmdata.serv=="Site" && this.siteservices) {
                services = this.siteservices;       // replace "Site" by list of siteservices
            }
            $$("#serv-select option").each( function(o) {
                o.select = services.some( function(item, index) { return item==o.value; });
                if (o.select) {
                    //o.setStyle("background-color", "#68B6FF");
                    //o.setStyle("color", "#ffffff");
                    o.setStyle("background-color", "#CCCCCC");
                    o.setStyle("color", "#000000");
                    if (!elems.length) o.selected = true;
                }
                else {
                    //o.setText("-"+o.value);
                    o.setStyle("background-color", "#ffffff");
                    o.setStyle("color", "#000000");
                }
            });
        }
    };

    // update time period UI state (periodgroup buttons)
    this.updatePeriodUI = function()
    {
        // make selected time period bold
        $$("#periodgroup input").removeClass("bold");
        $(gmdata.period).addClass("bold");

        // update continuous availability checkboxes
        $$(["reliability", "maintenance", "unknown", "oldalgo"]).each( function(el) {
            el.checked = (el.id==gmdata.metricName);
            el.disabled = gmdata.period=="latest";
        });
    };

    // update the whole UI state according to the settings in gmdata
    this.updateAllUI = function()
    {
        this.updateTopoUI();
        this.updateLayoutMetricUI();
        this.updateVoUI();
        this.updateServUI();
        this.updatePeriodUI();
    };


    // updates the explanation text and color key
    // (is called from gmdata.updateGridMap() after the view has been updated)
    this.updateCaption = function(gmdata)
    {
        var topo_cap = {
            "regions":  "Certified Production sites",
            "tiers":    "WLCG sites",
            "pps":      "Certified Pre-Production sites",
            "all":      "All sites known by GStat"
        };
        var size_cap = {
            "cpu":  "number of CPUs from GStat",
            "tc":   "number of CPUs from BDII",
            "rj":   "number of currently running jobs",
            "tcsi": "Installed Capacity",
            "rjsi": "kSI2k of currently running jobs"
        };

        $('caption').removeClass('loading');
        $('gridmapCanvasLoading').setStyle('display', 'none');
        var msg = "";
        if (has_properties(gmdata.metric.data)) {
            // overall description
            var latest = gmdata.period=="latest";
            var serv;

            // set up service name
            try {
                serv = $(gmdata.serv).value;
            }
            catch(e) {
                serv = gmdata.serv;
            }

            if (latest) {
                msg += "Latest SAM results, ";
            }
            msg += serv + " " + (latest?"Status":metricName_to_str(gmdata.metricName)) + ", ";

            msg += "for '" + gmdata.vo + "' VO, ";
            msg += timestamp_string(gmdata.period, gmdata.ts) + ".<br>";

            // draw color key
            if (latest) {
                $('colorkeyCanvas').setStyle("width", 220);
                gridmap_colorkey_status(colorkey, {width:210, height:20, space:5, caption:["maint", "down", "degraded", "ok"],
                    descr:{"maint":"Maint", "down":"Down", "degraded":"Degraded", "ok":"Ok"}, color:color_status});
            } else {
                $('colorkeyCanvas').setStyle("width", 170);
                gridmap_colorkey_percentage(colorkey, {width:160, height:20, n:8, caption:[0,25,50,75,100],
                    color:color_function(gmdata)});
            }
        }
        else {
            colorkey.clear();
            colorkey.paint();
        }

        var wlcg_vo = gmdata.vo=='Alice' || gmdata.vo=='Atlas' || gmdata.vo=='CMS' || gmdata.vo=='LHCb';
        if (has_properties(gmdata.layout.sites)) {
            msg += "Size of site rectangles is " + size_cap[gmdata.layoutMetric+(gmdata.layoutSi2k?"si":"")];
            if (gmdata.topo=="tiers") {
                msg += wlcg_vo ? " serving the '"+gmdata.vo+"' VO" : " serving a WLCG VO";
            }
            if (gmdata.layoutUseHist) {
                msg += " (historical CPU numbers)";
            }
            if (gmdata.layoutVOView) {
                msg += " (VOView is used)";
            }
            msg += ".<br>";
        }

        if (gmdata.topo=="all") {
            msg += "All " + (gmdata.topoDrillDown?gmdata.topoDrillDown:"") + " sites known by GStat";
            if (gmdata.layoutMetric!="cpu") {
                msg += " having data in BDII";
            }
        } else {
            var commitment = "";
            if (gmdata.topo=="tiers") {
                if (wlcg_vo && !gmdata.allwlcg) {
                    commitment = " with MoU commitment for '" + gmdata.vo + "'";
                }
            }
            if (gmdata.topoDrillDown) {
                if (gmdata.topo=="tiers") {
                    msg += "WLCG " + gmdata.topoDrillDown + " sites" + commitment;
                } else {
                    msg += (topo_cap[gmdata.topo]||gmdata.topo) + " of '" + gmdata.topoDrillDown + "' region";
                }
            } else {
                msg += (topo_cap[gmdata.topo]||gmdata.topo) + commitment + ", grouped by " + (gmdata.topo=="tiers"?"tiers":"regions");
            }
        }
        msg += ".";

        $("caption").setHTML(msg);

        // debug
        msg = "SQL: ";
        if (gmdata.metric) {
            msg += gmdata.metric.msec + " msec";
        }
        //$("sqltime").setText(msg);
        this.createHistoryString();
    };

    // create history string from current state and add it to the dhtmlHistory object
    this.createHistoryString = function() {
        var url = "#topo="+gmdata.topo + "&layout="+gmdata.layoutMetric + "&vo="+gmdata.vo + "&serv="+gmdata.serv;
        if (gmdata.topoDrillDown) {
            url += "&drilldown="+gmdata.topoDrillDown;
        }
        if (gmdata.showsitenames) {
            url += "&sitenames";
        }
        if (gmdata.layoutVOView) {
            url += "&voview";
        }
        if (gmdata.layoutUseHist) {
            url += "&usehist";
        }
        if (gmdata.layoutSi2k) {
            url += "&si2k";
        }
        if (gmdata.layoutStrict) {
            url += "&strict";
        }
        if (gmdata.showosgsites) {
            url += "&osg";
        }
        if (gmdata.allwlcg) {
            url += "&allwlcg";
        }
        if (gmdata.period != "latest") {
            url += "&period="+gmdata.period;
            url += "&ts="+gmdata.ts;
        }
        if (gmdata.metricName != "availability") {
            url += "&metric="+gmdata.metricName;
        }

        // add history entry
        dhtmlHistory.add(url, 1);
    };

    // initialize model from history string
    this.setFromHistoryString = function()
    {
        var currentHash = dhtmlHistory.getCurrentHash().split('&');
        var param = {};
        for (var i  = 0; i < currentHash.length; i++) {
            var parts = currentHash[i].split('=');
            param[unescape(parts[0])] = unescape(parts[1]);
        }
        // set defaults
        gmdata.setTopo(param.topo||"regions", param.drilldown||"");
        gmdata.setShowSitenames(!!param.sitenames);

        gmdata.setLayoutMetric(param.layout||"tc");
        gmdata.setLayoutVOView(!!param.voview);
        gmdata.setLayoutUseHist(!!param.hist);
        gmdata.setLayoutSi2k(!!param.si2k);
        gmdata.setLayoutStrict(!!param.strict);
        gmdata.setVo(param.vo||"OPS");
        gmdata.setServ(param.serv||"Site");
        gmdata.setTimestamp(param.ts||Math.floor(new Date().getTime()/1000));     // temporary
        gmdata.setPeriod(param.period||"latest");           // timestamp is updated after data is retrieved
        gmdata.setMetricName(param.metric||"availability");
        gmdata.setShowOsgSites(!!param.osg);
        gmdata.setAllWlcg(!!param.allwlcg);

        // update the UI elements
        this.updateAllUI();

        // validate timestamp and redraw gridmap
        this.periodUpDown(0);
    };


    // Initialize UI elements
    this.initialize = function()
    {
        var thisRef = this;

        // setup event handlers for topology selection
        $$('#topogroup input').addEvent("click", function() {thisRef.selectTopo(this);});

        // setup event handlers for layout metric selection
        $$('#layoutgroup input').addEvent("click", function() {thisRef.selectLayoutMetric(this);});

        // setup event handlers for VO selection
        $$('#vogroup input.vo-button').addEvent("click", function() {thisRef.selectVo(this);});
        $('vo').addEvent("click", function() {thisRef.selectVo(this);});
        $('vo').addEvent("change", function() {thisRef.selectVo(this);});
        $('vo').addEvent("submit", function() {thisRef.selectVo(this);});

        // setup event handlers for service selection
        $$('#servgroup input.serv-button').addEvent("click", function() {thisRef.selectServ(this);});
        $$(['serv']).addEvent("click", function() {thisRef.selectServ(this);});
        $$(['serv']).addEvent("change", function() {thisRef.selectServ(this);});
        $('serv-select').addEvent("change", function() {thisRef.selectServ(this);});

        // setup event handlers for time period selection
        $$('#periodgroup input.period-button').addEvent("click", function() {thisRef.selectPeriod(this);});
        $$('#periodgroup input.period-long-button').addEvent("click", function() {thisRef.selectPeriod(this);});
        $('period-up').addEvent("mousedown", function() {thisRef.periodUpDown(+1);});
        $('period-down').addEvent("mousedown", function() {thisRef.periodUpDown(-1);});

        // setup event handler for metric selection checkboxes
        $$(["reliability", "maintenance", "unknown", "oldalgo"]).addEvent("click", function() {thisRef.selectMetric(this);});

        // setup event handler for showing/hiding additional checkboxes
        $('ext-ui').addEvent("click", function() {
            if (gmdata.layoutStrict) {
                gmdata.setLayoutStrict(false);
                thisRef.updateLayoutMetricUI();
                gmdata.updateGridmap();
            }
            $$('span[id=more]').toggleClass('hidden');
        });

        // global change event
        // This didn't include changes triggered by the view (e.g. drillDown), therefore
        // the createHistoryString() call was moved to the updateCaption() function
        //$$('form').addEvent("click", function() { thisRef.createHistoryString(); });

        // get all avaliable SAM services and update the UI when they are received
        ajax_samservices(function(obj) {
            thisRef.drawServOptions(obj.allservices);
            thisRef.siteservices = obj.siteservices;    // remember siteservices for updateServUI()
            thisRef.updateServUI();
        });

        // INITIALIZE MODEL
        // function to call when timestamp is updated
        gmdata.setTimestampCallback( function(str) {
            $("period-ts").setText(str);
        });

        // function to call after the gridmap view has been updated
        gmdata.setUpdateCallback(function(gmdata) {thisRef.updateCaption(gmdata);});

        // set up the model from the current history string
        this.setFromHistoryString();

        // add history listner
        dhtmlHistory.addListener( function() { thisRef.setFromHistoryString(); });
    };
}
