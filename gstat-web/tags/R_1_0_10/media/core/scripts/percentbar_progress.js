/* Revision of WebAppers Progress Bar, version 0.2
*  (c) 2007 Ray Cheung
*  WebAppers Progress Bar is freely distributable under the terms of an Creative Commons license.
*  For details, see the WebAppers web site: http://wwww.Webappers.com/
/*--------------------------------------------------------------------------*/

var initial = -119;
var imageWidth = 240;
var eachPercent = (imageWidth/2)/100;
var DIR_PATH_IMAGES = "/media/core/scripts/img/"

/************************************************************/
function setText (id, percent)
{
    $(id+'Text').innerHTML = percent+"%";
}

/************************************************************/
function display ( total, used )
{	
    var percentage = 0;
    var color = 5;
    if (total!='N/A' && used!='N/A') {
        total = parseInt(total);
        used  = parseInt(used);
	    if (total != 0) percentage = parseInt(used * 100 / total);
	    else            percentage = 0;
	
	    if      (percentage < 0)   color = "2"; //yellow
	    else if (percentage < 80)  color = "1"; //green
	    else if (percentage < 90)  color = "2"; //yellow
	    else if (percentage < 101) color = "4"; //red
	    else                       color = "2"; //yellow
    }
    
    var percentageWidth = 0;
    if (percentage < 0 || percentage > 100) percentageWidth = eachPercent * 100;
    else percentageWidth = eachPercent * percentage;
    var actualWidth = initial + percentageWidth;
    document.write('<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage.png" ' + 
        'alt="'+percentage+'%" ' + 
        'class="percentImage'+color+'" ' +
        'style="background-position: '+actualWidth+'px 0px;"/> ' +
        '<span>'+percentage+'%</span>');
}

function display_string( total, used, type)
{	
    var percentage = 0;
    var color = 5;
    if (total != 0) percentage = parseInt(used * 100 / total);

    if (type == "usedonline") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 101) color = "4"; //red
        else                       color = "2"; //yellow
    } else if (type == "usednearline") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 101) color = "4"; //red
        else                       color = "2"; //yellow
    } else if (type == "runningjobs") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 10)  color = "4"; //red
        else if (percentage < 20)  color = "2"; //yellow
        else if (percentage < 201) color = "1"; //green
        else                       color = "2"; //yellow
    } else if (type == "waitingjobs") {
        if      (percentage < 0)   color = "2"; //yellow
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 101) color = "4"; //red
        else                       color = "2"; //yellow
    } else {
        if      (percentage < 0)   color = "5"; //gray
        else if (percentage < 80)  color = "1"; //green
        else if (percentage < 90)  color = "2"; //yellow
        else if (percentage < 95)  color = "3"; //orage
        else if (percentage < 101) color = "4"; //red
        else                       color = "5"; //gray 
    }

    var initial = -60;
    var imageWidth = 120;
    var eachPercent = (imageWidth/2)/100;
    var percentageWidth = 0;
    if (percentage < 0 || percentage > 100) percentageWidth = eachPercent * 100;
    else percentageWidth = eachPercent * percentage;
    var actualWidth = initial + percentageWidth;
    var content = '<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage_small.png" ' + 
        'alt="'+percentage+'%" ' + 
        'title="'+used+'" ' + 
        'class="percentImage'+color+'_small" ' +
        'style="background-position: '+actualWidth+'px 0px;"/> ' +
        '<span class="PercentageStatus'+color+'">'+percentage+'%</span>';
    return content;
}