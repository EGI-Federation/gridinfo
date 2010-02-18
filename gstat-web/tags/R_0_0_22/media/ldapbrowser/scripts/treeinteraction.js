function loadData(node, fnLoadComplete)  {
    var callback = {
        success: function(Response) {
		    var Results =  eval("(" + Response.responseText + ")");
		    YAHOO.log(Response.responseText, "info", "example");
		    if (Results && (Results.length > 0)) {
		        for (var i=0, j=Results.length; i<j; i++) {
		    		label = Results[i].substring(0, Results[i].indexOf(node.label)-1)
		            var newNode = new YAHOO.widget.MenuNode(label, node, false);
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
    var url = "/gstat/ldap/browse?host=" + host + "&dn=" + nodeLabel;
    YAHOO.util.Connect.asyncRequest('GET', url, callback);
}

function showEntry(node, fnLoadComplete)  {           
    var nodeLabel = encodeURI(node.title);
    var url = "/gstat/ldap/browse?host=" + host + "&entry=true&dn=" + nodeLabel;
    YAHOO.util.Dom.get('entry').data = url;
}

function buildTree() {
    var tree = new YAHOO.widget.TreeView("tree");
    tree.setDynamicLoad(loadData, 1);
    var root = tree.getRoot();
    var rootNode = new YAHOO.widget.MenuNode("o=grid", root, false);
    rootNode.title = "o=grid";
    tree.subscribe("labelClick", function(node){ showEntry(node) });
    tree.draw();
}