/** LDAP Host to connect to. Eg: ldap://bdii118.cern.ch:2170/ */
var selectedHost = '';
/** YUI TreeView object that represents the LDAP tree */
var tree;

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
		            var idx = Results[i].indexOf(node.label);
		            if (idx == 0) {
		                idx = Results[i].indexOf(node.label + ',');
		            }
                    var label = Results[i].substring(0, idx-1);
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
    window.location.hash ='#' + selectedHost + nodeLabel;
    var url = "/gstat/ldap/browse?host=" + selectedHost + "&entry=true&dn=" + nodeLabel; 
    var request = YAHOO.util.Connect.asyncRequest('GET', url, {success: handleSuccess});
}

/** Setup the tree when a host is selected */
function buildTree() {
    var tree = new YAHOO.widget.TreeView("tree");
    tree.setDynamicLoad(showNode, 1);
    var root = tree.getRoot();
    var rootNode = new YAHOO.widget.MenuNode("o=grid", root, true);
    rootNode.title = "o=grid";
    tree.subscribe("expand", function(node){ showEntry(node) });
    tree.draw();
}

/** Updates a tree path from an LDAP Route. Eg: mds-vo-name=local,o=grid */
function updateTree(ldapRoute) {
    var values = ldapRoute.split(',');
    var gridNode = tree.getRoot().children[0];
    var currentNode = gridNode;
    var currentText = 'o=grid';
    for (var i = values.length-1; i >= 0; i--) {
        if (values[i] != 'o=grid') {
            currentNode.expand();
            currentText = values[i] + ',' + currentText;
            var newNode = new YAHOO.widget.TextNode(values[i], currentNode, true);
            newNode.title = currentText;
            currentNode = newNode;
        }
    }
    showEntry(currentNode);
}

/** Builds a tree when a host is selected in the combobox */
function selectHost(selectobj) {
    var selectedHost = selectobj.options[selectobj.selectedIndex].value;
    var urltext = document.getElementById('urltext');
    urltext.value = selectedHost;
    window.location.hash ='#' + selectedHost;
    resetAttributesTable();
    buildTree();
}

/** Builds a tree when a host is typed manually */
function inputHost() {
    var urltext = document.getElementById('urltext');
    var selectedHost = urltext.value;
    var hosts = document.getElementById('hosts');
    hosts.selectedIndex = 0;
    window.location.hash ='#' + urltext;
    resetAttributesTable();
    buildTree();
}

/** To be executed when the page is loaded */
function init() {
    if (window.location.hash != '') {
        var hash = window.location.hash;
        var num = hash.indexOf('//');
        num = hash.indexOf('/', num + 2);
        var selectedHost = hash.substring(1, num + 1);
        document.getElementById('urltext').value = selectedHost;
        var ldapRoute = hash.substring(num + 1, hash.length);
        buildTree();
        updateTree(ldapRoute);
    }
};
