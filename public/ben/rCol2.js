function rCol2(parent){
    this.parent = parent;
    this.colname = "null";
    this.sources = [];
    var c = $("<div>");
    this.content = c;


    var bsize = 1;
    var msize = 5;
    var psize = 5;
    var height = parent.height() - bsize *2 - msize * 2 - psize* 2;

    c.css("border-style",'solid');
    c.css("border-width",bsize+'px');
    c.css("border-color",'#000000');
    c.css("margin",msize+'px');
    c.css("padding",psize+'px');
    c.css("position",'absolute');
    c.css("left",'0px');
    c.css("top",'0px');
    c.css("right",'0px');
    c.css("height",height);
       

    c[0].style.webkitTransitionProperty = '-webkit-transform';
    c[0].style.webkitTransitionTimingFunction = 'cubic-bezier(0,0,0.25,1)';
    c[0].style.webkitTransitionDuration = '400ms';
    c.column = this;


    var cbc = $("<div>");
    cbc.addClass("column_button_container");
    cbc.css("z-index",cbut_z_index);
    cbc.css("width","auto");
    cbc.css("height","auto");
    cbc.css("position","absolute");
    cbc.css("bottom","5px");
    cbc.css("left","5px");
    c.append(cbc);

    //Class methods.
    rCol2SetMethods(this);

    this.makeSubViews();


}
function rCol2SetMethods(rcol){
    
    rcol.setFilter = rCol2SetFilter;
    rcol.getFilter = rCol2GetFilter;
    rcol.computeFilter = rCol2ComputeFilter;

    rcol.addSource = rCol2AddSource;
    rcol.removeSource = rCol2RemoveSource;
    rcol.clearSources = rCol2ClearSources;
    rcol.getSources = rCol2GetSources;
    rcol.computeSources = rCol2ComputeSources;

    rcol.setItemClickedAction = rCol2SetItemClickedAction;
    rcol.getItemClickedAction = rCol2GetItemClickedAction;
    rcol.computeItemClickedAction = rCol2ComputeItemClickedAction;

    rcol.setDataType = rCol2SetDataType;
    rcol.getDataType = rCol2GetDataType;
    rcol.fetchData = rCol2FetchData;
    rcol.showData = rCol2ShowData;
    rcol.setData = rCol2SetData;

    
    rcol.makeSubViews = rCol2MakeSubViews;
    rcol.makeColumnControls = rCol2MakeColumnControls;

    //buttonClicked calls buttonSelected.
    rcol.buttonClicked = rCol2ButtonClicked;
    rcol.buttonSelected = rCol2ButtonSelected;

    rcol.listItemMouseEnter = rCol2ListItemMouseEnter;

}
function rCol2SetFilter(filter){
    this.filter = filter;
    this.filterHUD.update();

}
function rCol2ComputeFilter(){
    
}
function rCol2GetFilter(){
    return this.filter;
}

function rCol2AddSource(source){
    sources = this.sources;
    hasfound = false;
    $.each(sources,function(i,item){
	if(item == source){hasfound = true;}
    });
    if (! hasfound ){
	this.sources.push(source);
    }
}
function rCol2RemoveSource(source){
    sources = this.sources;
    $.each(sources, function(i,item){
	if(item == source){
	    sources.splice(i,1);
	    return false;
	}
    });
}
function rCol2ComputeSources(){
    var controls = this.content.find(".column_control");
    rcol = this;
    rcol.clearSources();
    $.each(controls,function(idx,item){
	jq = $(item);
	if( jq.hasClass('is_selected')){
	    if(jq[0].group == 'sourceSelects'){
		rcol.addSource(jq[0].cbutton_name)
	    }
	}
    });    
}
function rCol2GetSources(){
    return this.sources;
}
function rCol2ClearSources(){
    this.sources = [];
};

function rCol2SetItemClickedAction(action){
    this.itemClickedAction = action;
}
function rCol2ComputeItemClickedAction(type){
    //for now, the type argument is disregarded.
    var controls = this.content.find(".column_control");
    var output = 'default';
    $.each(controls,function(idx,item){
	jq = $(item);
	if( jq.hasClass('is_selected')){
	    if(jq[0].group == 'clickActionSelects'){
		output =  jq[0].cbutton_name;
	    }
	}
    });    
    this.clickaction = output;
}
function rCol2GetItemClickedAction(){
    return this.clickaction;
}
function rComputeItemClickedFilter(rcol,idx){


    d = rcol.data[idx];
    dtype = rcol.datatype;
    var filter = {};
    switch(dtype){
    case 'album':
	filter = {album_mbid:d['album_mbid']};
	break;
    case 'track':
	filter = {track_mbid:d['track_mbid']};
	break;
    case 'artist':
	filter = {artist_mbid:d['artist_mbid']};
	break;
    case 'member':
	filter = {artist_mbid:d['artist_mbid']};
    default:
	console.log('no filter for dtype: ' + dtype);
    }
    return filter;
}

function rCol2SetDataType(datatype){

    old_dt = this.getDataType();
    this.datatype = datatype;
    new_dt = this.getDataType();
 
    
    if (old_dt != new_dt){
	this.makeColumnControls();
    }
}
function rCol2GetDataType(){

    return this.datatype;
}

function rCol2MakeColumnControls(){
    makeAndStyleColumnControls(this);
}
function rCol2MakeSubViews(){

    var fhud = new filterHUD(this);
    this.filterHUD = fhud;
    this.content.append(this.filterHUD.content);  
    var ihud = new infoHUD(this);
    this.infoHUD = ihud;
    this.content.append(this.infoHUD.content);    
    
    var dv = new dataView(this);
    this.content.append(dv.content);
    this.dataview = dv.content;
    this.dataview_data_offsets = [];
    var dv_covers = [[this.content.find(".column_button_container")[0],'left'],
		    [ihud.content[0],'right']];
    dv.content[0].covers = dv_covers;
    dv.content[0].rcol = this;    

}

function rListItemClicked(rcol,idx){
    
    var d = rcol.data[idx];
    var dtype = rcol.getDataType();  
  
    rcol.computeItemClickedAction();
    var clickaction = rcol.getItemClickedAction();


    var trg = rGetColumnClickEventTargetColumn(rcol);
    trg.setFilter(rComputeItemClickedFilter(rcol,idx));


    switch(dtype){
    case 'album':
	switch(clickaction){
	case 'tracks':
	    trg.setDataType('track');
	    break;
	default:
	    console.log("unhandled album clickaction" + clickaction);
	    break;
	}
	break;
	
    case 'artist':
	switch(clickaction){
	case 'members':
	    trg.setDataType('member');
	    break;	    
	case 'albums':
	    trg.setDataType('album');
	    break;
	case 'tracks':
	    trg.setDataType('track');
	    break;
	default:
	    console.log("unhandled artist clickaction: " + clickaction);
	}
	break;
    case 'member':
	switch(clickaction){	    
	case 'albums':
	    trg.setDataType('album');
	    break;
	default:
	    console.log("unhandled member clickaction: " + clickaction);
	}
	break;
    default:
	console.log("clicks on column type: " + dtype + " not yet handled");
    }   

    trg.makeColumnControls();
    trg.fetchData();	    

}
function rCol2ListItemMouseEnter( idx){
    this.focused_data = this.data[idx];
    this.infoHUD.update();

}
function rCol2ButtonSelected(but){
    grp = but[0].group;
    if (rGroupIsExclusive(but[0].group)){
	var controls = this.content.find(".column_control");
	$.each(controls,function(idx,item){
	    jq = $(item);
	    if( jq.hasClass('is_selected')){
		if (jq[0].group == grp){
		    jq.removeClass('is_selected');
		}
	    }
	});
	but.addClass('is_selected');
    }  else {
	if (but.hasClass('is_selected') ){
	    but.removeClass('is_selected');
	} else {
	    but.addClass('is_selected');
	}
    }     

}
function rCol2ButtonClicked(but){
    this.buttonSelected(but);
    if (rButtonTriggersRefresh(but)){
	this.fetchData();
    }
}

function getFetchParams(rcol){
    rcol.computeFilter();
    rcol.computeSources();
    
    var request_srcs = {};
    $.each(rcol.getSources(),function(idx,r){
	var namestr = 'source' + idx;
	request_srcs[namestr] = r;
    });
    var action = '';
    switch(rcol.getDataType()){
    case 'track':
	action = 'tracks';
	break;
    case 'artist':
	action = 'artists';
	break;
    case 'album':
	action = 'albums';
	break;
    }
    
    var p = {filters:rcol.getFilter(),
	     action:action,
	     sources:request_srcs
	    };
    return p;
}
function rCol2FetchData(){
    var p= getFetchParams(this);
    var rcol = this;
    $.getJSON("/getsb/fetch2",p,function(data){
	rcol.showData(data);
    });

}
function rCol2SetData(data){
    this.data = data;
    if (data[0]['datatype'] != 'none'){
	    this.setDataType(data[0]['datatype']);

    }
}
function rCol2ShowData(data){   

    this.setData(data);
    ue = $("<ul>");
    ue.addClass("column_ul");    
    offsets = [];
    ue.append($("<div>").css("height",'25px'));
    les = [];
    les.length = data.length;

    var rcol = this;

    $.each(data,function(i,item){
	       var le = $("<li>");
	       item = mlinkedListItem(item,rcol);
	       le.append(item);
	       les[i] =le;
	       ue.append(le);

	
    });
    this.dataview.children().remove();
    this.dataview.append(ue);
    this.dataview_data_offsets = [];

    var this_col = this;
    $.each(les,function(i,le){
	this_col.dataview_data_offsets[i] = le[0].offsetTop;
    });
    
    rColumnHasBeenSet(this);

}


