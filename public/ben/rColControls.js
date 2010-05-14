
//Column Control Types Specifies the different controls that can appear over a column and whethe control governs the display of that column "internal", or the generation of another column "external".

//Indices denote: name, int/external,description,bgroup
var columnControlTypes = [
    ['members','external','click expands members','clickActionSelects'],
    ['albums','external','click expands albums','clickActionSelects'],
    ['mixed','internal','click chooses mixed source','sourceSelects'],
    ['remote','internal','click chooses internal source','sourceSelects'],
    ['local','internal','click chooses external source','sourceSelects'],
    ['tracks','external','click shows tracks','clickActionSelects']]
//'group names and exclusive/nonexclusive.'

var columnGroupsAreExclusive = {
    'clickActionSelects':1,
    'sourceSelects':0,
    'filterSelects':0   //note that filter selects is not implemented yet.
};

var cgColors = {
    'clickActionSelects':cbg_click_action_color,
    'sourceSelects':cbg_source_color,
    'filterSelects':cbg_filter_color  
};

function rccSelectOnInit(elt){
    if (elt.cbutton_name == 'local' ||
	elt.cbutton_name == 'remote' ||
	elt.cbutton_name == 'albums'){
	return true;
    }
    return false;
}

function rButtonTriggersRefresh(but){
    if( but[0].cbutton_action == 'internal'){
	return true;
    }
    return false;

}

function rGroupIsExclusive(groupname){
    val = columnGroupsAreExclusive[groupname];
    if (val == 1){
	return true;
    } else {
	return false;
    }
}

function makeAndStyleColumnControls(rcol){
    var datatype = rcol.getDataType();
    var controls;

    switch(datatype){
    case 'artist':
	controls = [0,1,3,4,5];
	break;
    case 'album':
	controls = [3,4,5];
	break;
    case 'track':
	controls = [3,4];
	break;
    case 'member':
	controls = [1,3,4];
	break;
    default:
	controls = [];
	break;
    } 
    
    //remove all current column buttons.
    var cbc = rcol.content.find(".column_button_container");
    cbc.children().remove();


    
    var cbGroups = {};
    for(var i = 0; i < controls.length ; i++){
	//pull the controls from the set of all column controls.
	var controlidx = controls[i];

	var name = columnControlTypes[controlidx][0];
	var action = columnControlTypes[controlidx][1];
	var description =  columnControlTypes[controlidx][2];
	var group = columnControlTypes[controlidx][3];

	var icon_src = "/icons2/"+name+"Button-med.png";
	var but = $("<a>");
	but[0].cbutton_name = name;
	but[0].cbutton_action=action;
	but[0].rcol = rcol;
	but[0].description = description;
	but[0].group = group;
		
	but.addClass("button");
	but.addClass("column_control");
	but.attr("href","#");
	
	var butimg = $("<img>");
	butimg.attr("src",icon_src);
	but.append(butimg);
	but.click(function(){ rcol.buttonClicked($(this));});
	but.hover(function(){setHUD($(this)[0].description);});

	if( ! cbGroups[group]){
	    var cbg = $("<div>");
	    cbg.addClass("column_button_group");
	    cbg.addClass("vertical_button_group");
	    cbg.css("border-color",cgColors[group]);
	    cbg.css("background-color", cbg_background_color);
	    cbc.append(cbg);
	    cbGroups[group] = cbg;
	}
	cbGroups[group].append(but);
	cbGroups[group].append("<br>");
    }
   
    $.each(cbGroups,function(idx,g){
	       $.each( g.find(".column_control"), function(idx,item){
			   if (rccSelectOnInit(item)){
			       rcol.buttonSelected($(item));
			   }
		       });
	   });
}


