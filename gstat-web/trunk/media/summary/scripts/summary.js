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

function changeFilterValue(event) {
    filtertype = document.getElementById('filtertype');
    filtervalue = document.getElementById('filtervalue');

    var oTable;
    var theads = $('#single_table > thead');
    $('#TableContainer').html('<table cellpadding="0" cellspacing="1" border="0" class="display" id="single_table"><thead>'+theads.html()+'</thead><tbody></tbody></table>');
    var oTable = $('#single_table').dataTable({
        "bProcessing": true, 
        "DisplayLength": 25, 
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
              "bUseRendered": false
            },
            { sWidth: null, sClass: 'master' },
            { sWidth: null },
            { sWidth: null },
            { "fnRender": function(oObj) {
                var used_space = display_string(oObj.aData[4], oObj.aData[5]);
                return used_space;
                },
              "bUseRendered": false
            },
            { sWidth: '16px', bSortable: false },
            { "fnRender": function(oObj) {
                var used_space = display_string(oObj.aData[3], oObj.aData[7]);
                return used_space;
                },
              "bUseRendered": false
            },
            { "fnRender": function(oObj) {
                var used_space = display_string(oObj.aData[6], oObj.aData[8]);
                return used_space;
                },
              "bUseRendered": false,
              sWidth: '110px'
            }]
    });
    oTable.fnReloadAjax("/gstat/summary/"+filtertype.value + "/" + encodeURIComponent(filtervalue.value) + "/json/");
    var value = $('#filtervalue :selected').val();
    //alert($('#sites_or_status').text());
    if (value=="" || value=="-1" || value=="ALL") $('#sites_or_status').text('Sites');
    else $('#sites_or_status').text('Monitoring Status');
}