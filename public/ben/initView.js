var myScroll1
var myScroll2
var isSmall
var isIpod

var infoShown = 0;

$(document).ready(function(){
    showHideInfo(0);

    maxwidth = (Math.max(screen.width,screen.height));
    initShared();
    if (maxwidth < 600){ isSmall = true } else {isSmall = false}
    if (isSmall){isIpod = true} else {isIpod = false}
    if (isSmall){
	initSmallView();
    } else {
	initBigView();
    }

    resetDimensions();
})

function resetDimensions(){
    h = viewHeight();
    w = viewWidth();
    $("#main_outer").height(h);
    $("#main_outer").width(w);
}

//Called with no argument, toggles infostate.
function showHideInfo(infoState){
    infoState = typeof(infoState) != 'undefined' ? infoState : 1 - infoShown;
    if (infoState){
	$("#info_main").css("visibility","visible");
    } else {
	$("#info_main").css("visibility","hidden");
    }
}

function viewWidth(){
    return window.innerWidth;
}
function viewHeight(){
    height = 0;
    if (isIpod){
	height = window.orientation == 90 || window.orientation == -90 ? 208 : 356;
    } else {
	height  = window.innerHeight;
	if (height> 500){height = 500}
    }
    return height;
}

function initShared(){
    var headID = document.getElementsByTagName("head")[0];         
    var cssNode = document.createElement('link');  
    cssNode.type = 'text/css';
    cssNode.rel = 'stylesheet';
    cssNode.href = '/ben/display2.css';
    cssNode.media = 'screen';
    headID.appendChild(cssNode);
}



function initSmallView(){
    var headID = document.getElementsByTagName("head")[0];             
    var meta =  document.createElement('meta');  
    meta.name="viewport";
    meta.content="width=device-width,minimum-scale=1.0, maximum-scale=1.0";
    headID.appendChild(meta);

    //Assume that we're working with an ipod... implement iscroll.
    window.addEventListener('orientationchange', small_setHeight);
    small_ready();
    //Set a timer to refresh iScroll once the page has loaded.
    window.onload = function() {setTimeout(function(){ small_refresh() }, 100)};
}

function small_ready() {
    myScroll1 = new iScroll('column1');
    myScroll2 = new iScroll('column2');
}
function small_refresh(){
    window.scrollTo(0, 1);
    myScroll1.refresh();
    myScroll2.refresh();
}

function small_setHeight() {
    //document.getElementById('wrapper').style.height = window.orientation == 90 || window.orientation == -90 ? '80px' : '200px';
}

function initBigView(){
    setTimeout(function(){ big_loaded() }, 100) ;
}
function big_loaded() {
    console.log("Loaded With 'Big' (non-ipod) View");
}

