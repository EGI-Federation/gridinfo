function loadJSONDoc(url) {
	$.ajax({
	    type: 'GET',
	    url: url,
	    dataType: 'json',
	    success: function(data){
		    clearList('filtervalue');
		    var select = document.getElementById('filtervalue');
		    appendToSelect(select, '-1', document.createTextNode('--SELECT A VALUE--'));
	        $.each(data.options, function(i,option){
	          if (option != null) {
	            appendToSelect(select, option.value, document.createTextNode(option.key));
	          }
	        });
	    },
	    data: {},
	    async: false
	});
}

// Invoked by "filtertype" select element change
// Clears "filtervalue" select and loads new values
function changeFilterType(evt) {
    // equalize W3C/IE event models to get event object
    evt = (evt) ? evt : ((window.event) ? window.event : null);
    if (evt) {
        // equalize W3C/IE models to get event target reference
        var elem = document.getElementById('filtertype');
        if (elem[elem.selectedIndex].value == 'none') {
        	changeFilterValue(evt);
        } else {
	        if (elem) {
	            try {
	                if (elem.selectedIndex > 0) {
	                    loadJSONDoc("/gstat/core/filter/" + elem.options[elem.selectedIndex].value);
	                }	
	            }
	            catch(e) {
	                var msg = (typeof e == "string") ? e : ((e.message) ? e.message : "Unknown Error");
	                alert("Unable to get JSON data:\n" + msg);
	                return;
	            }
	        }
	    }
    }
}

// empties a select list content
function clearList(listId) {
    var select = document.getElementById(listId);
    while (select.length > 0) {
        select.remove(0);
    }
}

// add item to select element the less
// elegant, but compatible way.
function appendToSelect(select, value, content) {
    var opt;
    opt = document.createElement("option");
    opt.value = value;
    opt.appendChild(content);
    select.appendChild(opt);
}
