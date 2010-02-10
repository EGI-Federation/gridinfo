function expandRow(rowID, clickRow) {
    var item = document.getElementById(rowID);
    if(item.className=='hidden') {
        //item.cells[0].innerHTML = StringToTalbe(item.cells[0].innerHTML);
        item.className = 'unhidden';
        clickRow.rowSpan=2;
        clickRow.innerHTML = '<img src="/media/gridsite/scripts/img/collapse.gif"/>';
    }else{
        item.className = 'hidden';
        clickRow.rowSpan=1;
        clickRow.innerHTML = '<img src="/media/gridsite/scripts/img/expand.gif"/>';
    }
    
}

function ErrorsToTable(str) {   
    var elements=str.split("\n");
    document.write('<table cellspacing="1" cellpadding="0" border="0" class="tablesorter">');
    for(i=0;i<elements.length-1;i++) {
      //table is begun outside the script, but need to open a table row 
      //for the first array item (elements[0]) OR for the fifth, ninth, etc.
      if(i==0) { document.write("<tr>"); }
      if(i%1 == 0 && i!=0) { document.write("<tr>"); }
	  //write in the element enclosed in <td> tags
	  document.write("<td>" + elements[i] + "</td>");
      //close the table row after the fourth, eighth, etc. item
      if(i%1 == 0) { document.write("</tr>"); }
    }
    document.write("</table>");
}

function DataSources(check_name) {
    var datasources = new Array();
	datasources["check-bdii-freshness"] = new Array("freshness","entries");
	datasources["check-bdii-sites"]     = new Array("time","entries");
	datasources["check-bdii-services"]  = new Array("time","entries");
	datasources["check-ce"]             = new Array("errors","warnings","info");
	datasources["check-sanity"]         = new Array("errors","warnings","info");
	datasources["check-se"]             = new Array("errors","warnings","info");
	datasources["check-service"]        = new Array("errors","warnings","info");
	datasources["check-site"]           = new Array("errors","warnings","info");

    return datasources[check_name];
}

function PageReload(timeout) {
    setTimeout('location.reload(true);',timeout); //300000, reload page every 5 minutes
}