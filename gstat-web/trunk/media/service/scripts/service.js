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

function changeServiceView(event) {
    var service_type = document.getElementById('services').value;
    if (service_type != "-1")
        window.open('/gstat/service/' + service_type, '_self')
}