function filterHUD(rcol){
    this.rcol = rcol;
    c = $("<div>");
    c.addClass("hud");
    c.addClass("filterHUD");
    c.css("position","absolute");
    c.css("background-color",filter_hud_background_color);
    c.css("bottom","5px");
    c.css("left","5px");
    c.css("right","5px");
    c.css("height",'auto');
    c.css("font-size",filter_hud_font_size);
    c.css("visibility","visible");
    c.css("z-index",hud_z_index);
    
    c.html("filter_html");
    this.content = c;

    this.show = filterHUDShow;
    this.hide = filterHUDHide;
    this.update = filterHUDUpdate;

    this.update();
    this.show();
}

function filterHUDShow(){
    this.content.css("visibility","visible");
}
function filterHUDHide(){
    this.content.css("visibility","hidden");
}
function filterHUDUpdate(){
    var str = 'filters: <br/>';
    var f = this.rcol.getFilter();
    if (f){
	$.each(f,function(key,item){
	    str = str + "Key: " + key + "  Item: " + item + "<br/>";
	});
    }
    this.content.html(str);
}

function infoHUD(rcol){
    this.hidetime = null;
    this.rcol = rcol;
    c = $("<div>");
    c.addClass("hud");
    c.addClass("info_hud");
    c.css("position","absolute");
    c.css("background-color",info_hud_background_color);
    c.css("top","20%");
    c.css("bottom","20%");
    c.css("left","50%");
    c.css("right","-20px");
    c.css("font-size",info_hud_font_size);
    c.css("visibility","visible");
    c.css("z-index",hud_z_index);
    
    this.content = c;

    this.show = infoHUDShow;
    this.hide = infoHUDHide;
    this.update = infoHUDUpdate;

    this.update();
    this.show();
}
function infoHUDShow(){
    this.content.css('visibility','visible');    
}
function infoHUDHide(){
    this.content.css('visibility','hidden');
}
function infoHUDUpdate(){
    var me = this;
    clearTimeout(this.hidetime);
    this.hidetime = setTimeout(function(){
			 me.hide();
		       }, 1000);

    me.show();
    var data = this.rcol.focused_data;
    if (! data){
    } else {

	var text = "";
	text += "<br/>";
	text += data['tostring'];
	text += "<br/>";
	this.rcol.computeItemClickedAction();
	text += "Clicking will result in retrieving: "+this.rcol.getItemClickedAction();
	this.content.html(text);

	
	var ul = $("<ul>");
	var li = $("<li>").html('Locations Available:').addClass('hud_list_header');

	ul.append(li);
	for (var i = 0 ; i < data['locations'].length ; i++){
	    li = $("<li>").html(data['locations'][i]).addClass('hud_list_item');
	    ul.append(li);
	}
	li = $("<li>").html('Other data:').addClass('hud_list_header');
 	ul.append(li);

	for (key in data){
	    var str = String(data[key]);
	    li = $("<li>").html(str).addClass('hud_list_item');
	    ul.append(li);
	}
	

	this.content.append(ul);

	
    }
}


function dataView(rcol){
    
    var dv = $("<div>");
    dv.css("width","auto");
    dv.css("height",'inherit');
    dv.css("postion","absolute");
    dv.css("overflow","scroll");
    dv.css("background-color",rcol_dataview_background_color);
    dv.mouseenter(uncoverDataView );
    dv.mouseleave(recoverDataView);
    this.content = dv;
    return this;

}


function uncoverDataView(){
    
    var rcol = this.rcol;
    var content = rcol.content;
    var cbc = content.find(".column_button_container");


    var covers = this.covers;
    $.each(covers, function(idx, item){
	       var elt = item[0];
	       var dir = item[1];
	       var timeout = 0;
	       var move_factor = .6;
	       var tform;
	       switch(dir){
	       case 'left':
		   tform = [-1*$(elt).width()*move_factor,0];
		   break;
	       case 'right':
		   tform = [1*$(elt).width()*move_factor,0];
		   break;
	       case 'up':
		   tform = [0,-1*$(elt).height()*move_factor];
		   break;
	       case 'down':
		   tform = [0,1*$(elt).height()*move_factor];
		   break;
	       }
	       elt.style.webkitTransitionProperty = '-webkit-transform';
	       elt.style.webkitTransitionTimingFunction = 'cubic-bezier(0,0,0.25,1)';
	       elt.style.webkitTransitionDuration = '600ms';
	       setTimeout(function(){elt.style.webkitTransform = 'translate3d('+ tform[0]+ 'px,' + tform[1]+ 'px,0)';	},timeout       );

	   }
	  );
}



function recoverDataView(){

    var rcol = this.rcol;
    var content = rcol.content;
    var cbc = content.find(".column_button_container");


    var covers = this.covers;
    $.each(covers, function(idx, item){
	       var timeout = 0;
	       var elt = item[0];
	       var dir = item[1];

	       elt.style.webkitTransitionProperty = '-webkit-transform';
	       elt.style.webkitTransitionTimingFunction = 'cubic-bezier(0,0,0.25,1)';
	       elt.style.webkitTransitionDuration = '300ms';
	       setTimeout(function(){elt.style.webkitTransform = 'translate3d('+ 0+ 'px,' + 0+ 'px,0)';	},timeout       );
	   }
	  );

}