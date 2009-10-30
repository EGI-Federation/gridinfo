/* Revision of WebAppers Progress Bar, version 0.2
*  (c) 2007 Ray Cheung
*  WebAppers Progress Bar is freely distributable under the terms of an Creative Commons license.
*  For details, see the WebAppers web site: http://wwww.Webappers.com/
/*--------------------------------------------------------------------------*/

var initial = -119;
var imageWidth = 240;
var eachPercent = (imageWidth/2)/100;
var DIR_PATH_IMAGES = "/media/summary/scripts/img/"

/************************************************************/
function setText (id, percent)
{
    $(id+'Text').innerHTML = percent+"%";
}

/************************************************************/
function display ( total, used )
{	
    if (total != 0) percentage = parseInt(used * 100 / total);
    else            percentage = 0;

  	if (percentage < 80) color = "1";
  	if (percentage >= 80 && percentage < 90) color = "2";
  	if (percentage >= 90 && percentage < 95) color = "3";
  	if (percentage >= 95) color = "4";
  	if (percentage < 0 || percentage > 100) color = "5";

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

function display_string( total, used )
{	
    if (total != 0) percentage = parseInt(used * 100 / total);
    else            percentage = 0;

  	if (percentage < 80) color = "1";
  	if (percentage >= 80 && percentage < 90) color = "2";
  	if (percentage >= 90 && percentage < 95) color = "3";
  	if (percentage >= 95) color = "4"; 
  	if (percentage < 0 || percentage > 100) color = "5";

    var percentageWidth = 0;
    if (percentage < 0 || percentage > 100) percentageWidth = eachPercent * 100;
    else percentageWidth = eachPercent * percentage;
    var actualWidth = initial + percentageWidth;
    var content = '<img ' +
        'src="'+DIR_PATH_IMAGES+'percentImage.png" ' + 
        'alt="'+percentage+'%" ' + 
        'title="'+used+'" ' + 
        'class="percentImage'+color+'" ' +
        'style="background-position: '+actualWidth+'px 0px;"/> ' +
        '<span class="PercentageStatus'+color+'">'+percentage+'%</span>';
    return content;
}

/************************************************************/
function emptyProgress(id)
{
    var newProgress = initial+'px';
    $(id).style.backgroundPosition=newProgress+' 0';
    setText(id,'0');
}

/************************************************************/
function getProgress(id)
{
    var nowWidth = $(id).style.backgroundPosition.split("px");
    return (Math.floor(100+(nowWidth[0]/eachPercent))+'%');
	
}

/************************************************************/
function setProgress(id, percentage)
{
    var percentageWidth = eachPercent * percentage;
    var newProgress = eval(initial)+eval(percentageWidth)+'px';
    $(id).style.backgroundPosition=newProgress+' 0';
    setText(id,percentage);
}

/************************************************************/
function plus ( id, percentage )
{
    var nowWidth = $(id).style.backgroundPosition.split("px");
    var nowPercent = Math.floor(100+(nowWidth[0]/eachPercent))+eval(percentage);
    var percentageWidth = eachPercent * percentage;
    var actualWidth = eval(nowWidth[0]) + eval(percentageWidth);
    var newProgress = actualWidth+'px';
    if(actualWidth>=0 && percentage <100)
    {
        var newProgress = 1+'px';
        $(id).style.backgroundPosition=newProgress+' 0';
        setText(id,100);
        alert('full');
    }
    else
    {
        $(id).style.backgroundPosition=newProgress+' 0';
        setText(id,nowPercent);
    }
}

/************************************************************/
function minus ( id, percentage )
{
    var nowWidth = $(id).style.backgroundPosition.split("px");
    var nowPercent = Math.floor(100+(nowWidth[0]/eachPercent))-eval(percentage);
    var percentageWidth = eachPercent * percentage;
    var actualWidth = eval(nowWidth[0]) - eval(percentageWidth);
    var newProgress = actualWidth+'px';
    if(actualWidth<=-120)
    {
        var newProgress = -120+'px';
        $(id).style.backgroundPosition=newProgress+' 0';
        setText(id,0);
        alert('empty');
    }
    else
    {
        $(id).style.backgroundPosition=newProgress+' 0';
        setText(id,nowPercent);
    }
}

/************************************************************/
function fillProgress(id, endPercent)
{
    var nowWidth = $(id).style.backgroundPosition.split("px");
    startPercent = Math.ceil(100+(nowWidth[0]/eachPercent))+1;
    var actualWidth = initial + (eachPercent * endPercent);
    if (startPercent <= endPercent && nowWidth[0] <= actualWidth)
    {
        plus(id,'1');
        setText(id,startPercent);
        setTimeout("fillProgress('"+id+"',"+endPercent+")",10);
    }
}

