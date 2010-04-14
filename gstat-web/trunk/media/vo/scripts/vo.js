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

function loadTable(table, title) {
    var vo_name = window.location.href.split("/")[5];
    TableToolsInit.sPrintMessage = title + " Report for VO " + vo_name + " Provided by <a href='https://svnweb.cern.ch/trac/gridinfo/'> GStat 2.0 </a>";
    var oTable;
    var oTable = table.dataTable({
        "bProcessing": true,
        "iDisplayLength":10,
        "sDom": 'lfTrtip',
        "fnFooterCallback": function ( nRow, aaData, iStart, iEnd, aiDisplay ) {
            var total_job      = 0;
            var running_job    = 0;
            var waiting_job    = 0;
            var free_job_slot  = 0;
            
            for ( var i=0 ; i<aaData.length ; i++ ) {
                total_job     += parseInt(aaData[i][1]);
                running_job   += parseInt(aaData[i][2]);
                waiting_job   += parseInt(aaData[i][3]);
                free_job_slot += parseInt(aaData[i][4]);
            }
            
            var nCells = nRow.getElementsByTagName('th');
            nCells[1].innerHTML = CommaFormatted(total_job);
            nCells[2].innerHTML = CommaFormatted(running_job);
            nCells[3].innerHTML = CommaFormatted(waiting_job);
            nCells[4].innerHTML = CommaFormatted(free_job_slot);
	    }
       
       });

    oTable.fnReloadAjax("/gstat/vo/"+vo_name+"/"+table.attr('name')+"/json/");
    $('#'+table.attr('id')+'_processing').prepend( $('<img></img>').attr({'src':'/media/core/css/img/loading.gif'}).css({padding: '0px 8px'}) );

}