
function CommaFormatted(amount)
{   
    var isInt=parseInt(amount);
    if (isNaN(isInt)) return amount; 
    if (isInt == 0) return 0;
    isInt=isInt.toString().replace(/^0+/, ''); 
	isInt += '';
	x = isInt.split('.');
	x1 = x[0];
	x2 = x.length > 1 ? '.' + x[1] : '';
	var rgx = /(\d+)(\d{3})/;
	while (rgx.test(x1)) {
		x1 = x1.replace(rgx, '$1' + ',' + '$2');
	}
	return x1 + x2;
}

//To remove the comma for the variables
function RemoveCommaFormatted(amount) {
  amount= amount.replace(/,/g,"");
  return amount;
}

function TimeFormat(ms) {
    var isInt=parseInt(ms);
    if (isNaN(isInt)) {
        document.write("N/A"); 
    } else {
	    var m_names = new Array("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec");
	    if (ms != undefined) {
		    var d = new Date(parseInt(ms) * 1000);
		    var curr_date = d.getUTCDate();
		    var curr_month = d.getUTCMonth();
		    //curr_month++;
		    var curr_year = d.getUTCFullYear();
		    var curr_hour = d.getUTCHours();
		    var curr_min = d.getUTCMinutes();
		    var curr_sec = d.getUTCSeconds();
		    document.write(curr_date+"-"+m_names[curr_month]+"-"+curr_year+" "+curr_hour+":"+curr_min+":"+curr_sec+" UTC");
	    }
    }
}