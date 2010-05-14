var myScroll1;
var myScroll2;
var isSmall;
var isIpod;

$(document).ready(function(){

    var headID = document.getElementsByTagName("head")[0];         
    var cssNode = document.createElement('link');  
    cssNode.type = 'text/css';
    cssNode.rel = 'stylesheet';
    cssNode.href = '/ben/display2.css';
    cssNode.media = 'screen';
    headID.appendChild(cssNode);

    if (viewWidth() < 600){ isSmall = true; } else {isSmall = false; }
    if (isSmall){isIpod = true;} else {isIpod = false;}
    if (isSmall){
	var headID = document.getElementsByTagName("head")[0];             
	var meta =  document.createElement('meta');  
	meta.name="viewport";
	meta.content="width=device-width,minimum-scale=1.0, maximum-scale=1.0";
	headID.appendChild(meta);

	//Assume that we're working with an ipod... implement iscroll.
	window.addEventListener('orientationchange', resetDimensions);
	document.ontouchmove = function(e) { e.preventDefault(); return false; };
	myScroll1 = new iScroll('column1');
	myScroll2 = new iScroll('column2');
    } 

    

    window.onload = function() {setTimeout( resetDimensions , 100);};
})

var mc_style = 'equal';
var mc_filters = [];
var mc_types = [];
var mc_sources = [];
var mc_objects = [];

var mc_ids = [];
var mc_clicktypes=['default','default']
var mc_clickactions=['default','default']

var mc_offsets = [[],[]];
var mc_data = [[],[]];
var mc_scroll_ids = ['column1','column2'];

function resetDimensions(){
    h = viewHeight();
    w = viewWidth();
    if (isIpod){vbump = 60;} else{vbump = 0}


    //reset the dimensions of the outer container
    mo =  $("#main_outer");
    hout = h - (mo.outerHeight() - mo.height()) + vbump;
    wout = w - (mo.outerWidth() - mo.width());
    mo.height(hout);
    mo.width(wout);
    
    //display dimensions.
    md = $("#main_display");
    hin = hout - (md.outerHeight() - md.height());
    win = wout - (md.outerWidth() - md.width());
    md.width(win);
    md.height(hin);


    //main column dimensions.
    mcs = $(".main_column");
    ncols = mcs.length;
    mc_props = [];
    
    
    for (i = 0 ; i < ncols ; i++){
	if (mc_style == 'equal'){mc_props.push(1/ncols)}
    }

    width_available = md.width();
    wids_so_far = 0;

    var rcol;
    $.each(mcs, function(i,item){
	mc = $(item);
	mc_objects[i] = mc;
	mc_ids[i] = mc.attr('id');
	
	mc_sources[i] = 'local';
	mc_filters[i] = {};
	mc_types[i] = 'none';

	this_wid = width_available*mc_props[i];
	mc.width(this_wid -(mc.outerWidth() - mc.width()));
	mc.height('200px');
	mc.css("background-color","00FF00");
	rcol = rManagerMakeColumn();
	mc.append(rcol.content);
    });

    styleControls();
    setTimeout(function(){ refreshScrolls() }, 100);

}

function viewWidth(){
    if (isIpod){
	w = window.orientation == 90 || window.orientation == -90 ? window.innerWidth : window.innerWidth;
    } else {
	w = screen.availWidth;

    }
    return w;
    
}
function viewHeight(){
    height = 0;
    if (isIpod){height = window.orientation == 90 || window.orientation == -90 ? 208 : 356;
	       } else {
		   height  = window.innerHeight;
		   if (height> 500){height = 500}
	       }
    return height;
}

function refreshScrolls(){
    if (isSmall){
	window.scrollTo(0, 1);
	myScroll1.refresh();
	myScroll2.refresh();
    }
}


var hud_timer = null;
function setHUD(strval){
    if (!strval){return}
    if (hud_timer){
	clearTimeout(hud_timer);
	hud_timer=null;
    }
    hud = $("#HUD");
    hudbg = $("#HUD_BG");
    hudtext = $("#HUD_TEXT");
    hudtext.html(strval);
    hud.css("visibility",'visible');
    hud_timer= setTimeout( hideHUD , 1000);
}
function hideHUD(){
    $("#HUD").css("visibility",'hidden');
    hud_timer=null;
}
