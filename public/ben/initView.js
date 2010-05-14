var myScroll1;
var myScroll2;
var isSmall;
var isIpod;

$(document).ready(function(){
    if (isSmall){isIpod = true;} else {isIpod = false;}
    window.onload = function() {setTimeout( resetDimensions , 100);};
});

var mc_style = 'equal';

function resetDimensions(){
    h = viewHeight();
    w = viewWidth();
    if (isIpod){vbump = 60;} else{vbump = 0}

    
    //reset the dimensions of the outer container
    mo =  $("#main_outer");
    hout = h - (mo.outerHeight() - mo.height()) + vbump ;
    wout = w - (mo.outerWidth() - mo.width());
    mo.height(hout);
    mo.width(w);
    
    //display dimensions.
    md = $("#main_display");
    hin = hout - (md.outerHeight() - md.height());
    win = wout - (md.outerWidth() - md.width());
    md.width(win);
    md.height(hin);


    //main column dimensions.

    var ncols = 2;
    var mcs = [];
    for ( var i = 0 ;  i < ncols ; i++){
	var mc = $("<div>");
	mc.addClass("main_column");
	mcs.push(mc);
	md.append(mc);
    }
    
    var mc_props = [];
    for (var i = 0 ; i < ncols ; i++){
	if (mc_style == 'equal'){mc_props.push(1/ncols)}
    }

    var width_available = md.width();
    var wids_so_far = 0;
    var rcol;
    $.each(mcs, function(i,item){
	       var mc = item;

	       var this_wid = width_available*mc_props[i];
	       mc.width(this_wid -(mc.outerWidth() - mc.width()));
	       rcol = rManagerMakeColumn(mc);
	       mc.append(rcol.content);
    });

    
    initMainControls();
    styleControls();
}

function viewWidth(){
    if (isIpod){
	w = window.orientation == 90 || window.orientation == -90 ? window.innerWidth : window.innerWidth;
    } else {
	w = window.innerWidth;

    }
    return w;
    
}
function viewHeight(){
    height = 0;
    if (isIpod){height = window.orientation == 90 || window.orientation == -90 ? 208 : 356;
	       } else {
		   height  = window.innerHeight;
	       }
    return height;
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
