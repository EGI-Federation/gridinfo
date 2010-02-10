var selectedHost = '';

/** Empty Attributes Table */
function resetAttributesTable()  {
	var entrypage = document.getElementById('entrypage');
	while(entrypage.hasChildNodes()) {
		entrypage.removeChild(entrypage.firstChild);
	}
}

/** Show more nodes of the tree */
function showNode(node, fnLoadComplete)  {
    var callback = {
        success: function(Response) {
		    var Results =  eval("(" + Response.responseText + ")");
		    if (Results && (Results.length > 0)) {
		        for (var i=0, j=Results.length; i<j; i++) {
                    label = Results[i].substring(0, Results[i].indexOf(node.label)-1);
		            var newNode = new YAHOO.widget.TextNode(label, node, false);
                    newNode.title = Results[i];
                }
            }
            Response.argument.fnLoadComplete();
        },
        failure: function(Response) {
            Response.argument.fnLoadComplete();
        },
        argument: {
            "node": node,
            "fnLoadComplete": fnLoadComplete
        },
        timeout: 7000
    };
            
    var nodeLabel = encodeURI(node.title);
    var url = "/gstat/ldap/browse?host=" + selectedHost + "&dn=" + nodeLabel;
    YAHOO.util.Connect.asyncRequest('GET', url, callback);
}

/** Show attributes of a concrete node */
function showEntry(node, fnLoadComplete)  {
    var handleSuccess = function(o){
        var div = document.getElementById('entrypage');
        if(o.responseText !== undefined){
            div.innerHTML = o.responseText;
		    $(document).ready(function() { 
		        $("#attributestable").tablesorter({sortList:[[0,0],[1,0]], widgets: ['zebra']}); 
		    });  

        }
    }
    var nodeLabel = encodeURI(node.title);
    var url = "/gstat/ldap/browse?host=" + selectedHost + "&entry=true&dn=" + nodeLabel; 
    //alert(url);
    var request = YAHOO.util.Connect.asyncRequest('GET', url, {success: handleSuccess});
}

/** Setup the tree when a host is selected */
function buildTree() {
    var tree = new YAHOO.widget.TreeView("tree");
    tree.setDynamicLoad(showNode, 1);
    var root = tree.getRoot();
    var rootNode = new YAHOO.widget.MenuNode("o=grid", root, false);
    rootNode.title = "o=grid";
    tree.subscribe("expand", function(node){ showEntry(node) });
    tree.draw();
}

/** Builds a tree when a host is selected in the combobox */
function selectHost(selectobj){
    selectedHost = selectobj.options[selectobj.selectedIndex].value;
    var urllink = document.getElementById('urllink');
    urllink.href = '/gstat/ldap/site/' + selectobj.options[selectobj.selectedIndex].text;
    var urltext = document.getElementById('urltext');
    urltext.value = selectedHost;
    resetAttributesTable();
    buildTree();
}

/** Builds a tree when a host is selected in the combobox */
function inputHost(){
    var urltext = document.getElementById('urltext');
    selectedHost = urltext.value;
    var urllink = document.getElementById('urllink');
    urllink.href = '/gstat/ldap/server/' + selectedHost;
    var hosts = document.getElementById('hosts');
    hosts.selectedIndex = 0;
    resetAttributesTable();
    buildTree();
}

/** Select the default host if needed */
function init() {
    var selectobj = document.getElementById('hosts');
    if (selectobj.options[selectobj.selectedIndex].value != "default") {
        selectHost(selectobj);
    } else {
    	inputHost();
    }
};
