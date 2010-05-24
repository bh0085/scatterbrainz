function mlink(type,data,rcol,str){
    if (!str){
	str = data['tostring'];
    }

    var content = $("<a>").addClass("mlink").attr("href","#").html(data['tostring'])[0];
    content.rcol=rcol;
    content.mldata=data;
    content.mltype=type;
    $(content).click(mlinkClicked);
    $(content).mouseenter(mlinkEntered);
    return content;

}

function mlinkedListItem(d,rc){
    var elt = $("<ul>").addClass('dataview_list_item');

    var main_type = d['datatype'];
    var str =  d['tostring'];
    var header =  $("<li>").append($(mlink(main_type,d,rc,str)).addClass('dataview_list_item_header'));
    elt.append(header);
    
    if (d['elements'].length > 1){
	$.each(d['elements'],function(idx,item){
		   var dt = item['datatype'];
		   str = item['tostring'];
		   var li = $("<li>").append($( mlink(dt,item,rc,str)));
		   li.addClass('dataview_sub_list_item');
		   elt.append(li);
	       });
    }
    
    return elt;
    
}

function mlinkEntered(){
    this.rcol.focused_data = this.mldata;
    this.rcol.infoHUD.update();
}
function mlinkClicked(){
    var action = mlinkClickAction(this);
    var filter = mlinkClickFilter(this);
    var sources = mlinkClickSources(this);
    var trg = mlinkClickTarget(this);
    if (action == 'default' || filter =={} || sources == []){
	console.log('click action unspecified');
    }

    //some nastiness to package the sources array
    var request_srcs = {};
    $.each(sources,function(idx,r){
	var namestr = 'source' + idx;
	request_srcs[namestr] = r;
    });

    var p = {filters:filter,
	     action:action,
	     sources:request_srcs
	    };

    $.getJSON("/getsb/fetch2",p,function(data){
	trg.showData(data);
    });

    
}
function mlinkClickTarget(link){
    return rGetColumnClickEventTargetColumn(link.rcol);
}
function mlinkClickSources(link){
    return rcol.getSources();
}
function mlinkClickFilter(link){
    var d = link.mldata;
    var filter = {}
    switch (link.mltype){
    case 'artist':
	filter['artist_mbid'] = d['artist_mbid'];
	break;
    case 'album':
	filter['album_mbid'] = d['album_mbid'];
	break;
    } 
    return filter;
}
function mlinkClickAction(link){
    var rcol = link.rcol;
    rcol.computeItemClickedAction();
    var action = rcol.getItemClickedAction(link.mltype);
    if ( action == 'default'){
	switch(link.mltype){
	case 'album':
	    action = 'tracks';
	    break;
	case 'artist':
	    action = 'albums';
	    break;
	}
    }
    return action;
}
