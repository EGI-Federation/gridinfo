$.fn.dataTableExt.oApi.fnReloadAjax = function (oSettings, sNewSource, fnCallback) {
    if ( typeof sNewSource != 'undefined' ) {
        oSettings.sAjaxSource = sNewSource;
     }
    this.fnClearTable( this );
    this.oApi._fnProcessingDisplay( oSettings, true );
    var that = this;

    $.getJSON( oSettings.sAjaxSource, null, function(json) {
        /* Got the data - add it to the table */
        for ( var i=0 ; i<json.aaData.length ; i++ ) {
            that.oApi._fnAddData( oSettings, json.aaData[i] );
        }
        oSettings.aiDisplay = oSettings.aiDisplayMaster.slice();
        that.fnDraw( that );
        that.oApi._fnProcessingDisplay( oSettings, false );
        /* Callback user function - for event handlers etc */
        if ( typeof fnCallback == 'function' ) {
            fnCallback( oSettings );
        }
    } );
}

jQuery.fn.dataTableExt.oSort['num-html-asc']  = function(a,b) {
	var x = a.toString().replace( /<.*?>/g, "" );
	var y = b.toString().replace( /<.*?>/g, "" );
	x = parseFloat( x );
	y = parseFloat( y );
	return ((x < y) ? -1 : ((x > y) ?  1 : 0));
};

jQuery.fn.dataTableExt.oSort['num-html-desc'] = function(a,b) {
	var x = a.toString().replace( /<.*?>/g, "" );
	var y = b.toString().replace( /<.*?>/g, "" );
	x = parseFloat( x );
	y = parseFloat( y );
	return ((x < y) ?  1 : ((x > y) ? -1 : 0));
};


var status = new Array();
status['ok'] = 1;
status['warning'] = 2;
status['critical'] = 3;
status['unknown'] = 4;
status['pending'] = 5;
status['n/a'] = 6;

jQuery.fn.dataTableExt.oSort['status-asc']  = function(a,b) {
    try { // status string
        a = a.toLowerCase();
        b = b.toLowerCase();
        return ((status[a] < status[b]) ? -1 : ((status[a] > status[b]) ?  1 : 0));
    } catch(err) { // site number
        return a - b;
    }
};

jQuery.fn.dataTableExt.oSort['status-desc'] = function(a,b) {
    try { // status string
        a = a.toLowerCase();
        b = b.toLowerCase();
        return ((status[a] < status[b]) ? 1 : ((status[a] > status[b]) ?  -1 : 0));
    } catch(err) { // site number
        return b - a;
    }
};

function changeFilterValue(event) {
    filtertype = document.getElementById('filtertype').value;
    filtervalue = document.getElementById('filtervalue').value;
    window.location.href = '/gstat/summary/' + filtertype + '/' + filtervalue;
}


function loadTable(event) {
    filtertype = document.getElementById('filtertype').value;
    filtervalue = document.getElementById('filtervalue').value;
    
    var oTable;
    var theads = $('#single_table > thead');
    $('#TableContainer').html('<table cellpadding="0" cellspacing="1" border="0" class="display" id="single_table"><thead>'+theads.html()+'</thead><tbody></tbody><tfoot><tr><th>Total</th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th><th></th></tr></tfoot></table>');
    var oTable = $('#single_table').dataTable({
        "iDisplayLength": 25, 
        "bProcessing": true, 
        "sDom": 'T<"clear">lfrtip',
        "aoColumns": [
            { sWidth: '50px', sClass: 'orderAction',
              "fnRender": function(oObj) {
                 var link = '';
                 var type = $('#filtertype :selected').val();
                 var value = $('#filtervalue :selected').val();
                 if (value=="" || value=="-1" || value=="ALL") 
                   link = '<a href="/gstat/summary/'+type+'/'+oObj.aData[0]+'/">'+oObj.aData[0]+'</a>';
                 else 
                   link = '<a href="/gstat/site/'+oObj.aData[0]+'/">'+oObj.aData[0]+'</a>';
   
                 return link;
                },
              "bUseRendered": false
            },
            { "fnRender": function(oObj) {
                 var status = '<span class="NagiosStatus_'+oObj.aData[1]+'">'+oObj.aData[1]+'</span>';
                 return status;
                },
              "bUseRendered": false,
              "sType": "status"
            },
            { "fnRender": function(oObj) {
                var physical_cpu = CommaFormatted(oObj.aData[2]);
                return physical_cpu
                },
              "bUseRendered": false,
              "bSearchable": false
            },
            { "fnRender": function(oObj) {
                var logical_cpu = CommaFormatted(oObj.aData[3]);
                return logical_cpu
                },
              "bUseRendered": false,
              "bSearchable": false
            },
            { "fnRender": function(oObj) {
                var total_online = CommaFormatted(oObj.aData[4]);
                return total_online;
                },
              "bUseRendered": false,
              "bSearchable": false
            },
            { "fnRender": function(oObj) {
                var used_online = display_string(oObj.aData[4], oObj.aData[5], "usedonline");
                return used_online;
                },
              "bSearchable": false,
              "sType": "num-html"
            },
            { "fnRender": function(oObj) {
                var total_nearline = CommaFormatted(oObj.aData[6]);
                return total_nearline;
                },
              "bUseRendered": false,
              "bSearchable": false
            },
            { "fnRender": function(oObj) {
                var used_nearline = display_string(oObj.aData[6], oObj.aData[7], "usednearline");
                return used_nearline;
                },
              "bSearchable": false,
              "sType": "num-html"
            },
            { "fnRender": function(oObj) {
                var total_job = CommaFormatted(oObj.aData[8]);
                return total_job;
                },
              "bUseRendered": false,
              "bSearchable": false
            },
            { "fnRender": function(oObj) {
                var running_job = display_string(oObj.aData[3], oObj.aData[9], "runningjobs");
                return running_job;
                },
              "bSearchable": false,
              "sType": "num-html"
            },
            { "fnRender": function(oObj) {
                var waiting_job = display_string(oObj.aData[8], oObj.aData[10], "waitingjobs");
                return waiting_job;
                },
              "bSearchable": false,
              "sType": "num-html" 
            }],
            "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
                var site           = 0;
                var physical_cpu   = 0;
                var logical_cpu    = 0;
                var total_online   = 0;
                var used_online    = 0;
                var total_nearline = 0;
                var used_nearline  = 0;
                var total_job      = 0;
                var running_job    = 0;
                var waiting_job    = 0;
                
                var calculate_site = false;
                var value = $('#filtervalue :selected').val();
                if (value=="" || value=="-1" || value=="ALL") calculate_site = true;
                
                for ( var i=0 ; i<aaData.length ; i++ ) {
                    if (calculate_site) site += parseInt(aaData[i][1].toString().replace( /<.*?>/g, "" ));
                    physical_cpu   += aaData[i][2];
                    logical_cpu    += aaData[i][3];
                    total_online   += aaData[i][4];
                    used_online    += parseInt(eval(aaData[i][5].split("title=")[1].split(" ")[0]));
                    total_nearline += aaData[i][6];
                    used_nearline  += parseInt(eval(aaData[i][7].split("title=")[1].split(" ")[0]));
                    total_job      += aaData[i][8];
                    running_job    += parseInt(eval(aaData[i][9].split("title=")[1].split(" ")[0]));
                    waiting_job    += parseInt(eval(aaData[i][10].split("title=")[1].split(" ")[0]));
                }
                
                /* Calculate the market share for browsers on this page */
                //for ( var i=iStart ; i<iEnd ; i++ ) {
                //  physical_cpu += aaData[aiDisplay[i]][2];
                //  logical_cpu  += aaData[aiDisplay[i]][3];
                //  total_space  += aaData[aiDisplay[i]][4];
                //  used_space   += aaData[aiDisplay[i]][5];
                //  total_job    += aaData[aiDisplay[i]][6];
                //  running_job  += aaData[aiDisplay[i]][7];
                //  waiting_job  += aaData[aiDisplay[i]][8];
                //}
                
                var nCells = nRow.getElementsByTagName('th');
                if (calculate_site) nCells[1].innerHTML = CommaFormatted(site);
                nCells[2].innerHTML = CommaFormatted(physical_cpu);
                nCells[3].innerHTML = CommaFormatted(logical_cpu);
                nCells[4].innerHTML = CommaFormatted(total_online);
                nCells[5].innerHTML = CommaFormatted(used_online);
                nCells[6].innerHTML = CommaFormatted(total_nearline);
                nCells[7].innerHTML = CommaFormatted(used_nearline);
                nCells[8].innerHTML = CommaFormatted(total_job);
                nCells[9].innerHTML = CommaFormatted(running_job);
                nCells[10].innerHTML = CommaFormatted(waiting_job);
		    }
    });
    
    if ($("#filtervalue").children().length > 1 && $("#filtervalue :selected").val() == "-1" ) 
        $("#filtervalue :selected").val("ALL");
    
    oTable.fnReloadAjax("/gstat/summary/"+filtertype+"/"+filtervalue+"/json/");
    var value = $('#filtervalue :selected').val();
    //alert($('#sites_or_status').text());
    if (value=="" || value=="-1" || value=="ALL") $('#sites_or_status').text('Sites');
    else $('#sites_or_status').text('Monitoring Status');
    
    if (!event) 
      setTimeout('loadTable();',300000); //Reload Ajax every 5 minutes
    //else
    //  $(document).ready(function() {window.location.href = '/gstat/summary/'+ filtertype + '/' + filtervalue;return true;});


}
