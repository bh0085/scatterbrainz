var c0Contents
var c1Contents
var c0Offsets
var c1Offsets


var c0id = "#scrollcol1";
var c1id = "#scrollcol2";


var writeColumn = 0;


function advanceCurrentColumn(){
    writeColumn = 1-writeColumn;
}
function mcCurrent(){
    return writeColumn;
}
//if mcNext is called with no argument
//it returns the next column for the
//current column
function mcNext(cur){
    cur = cur >=0  ? cur : mcCurrent();
    var next = cur + 1;
    if (next >= mcNum()){next = 0;}
    return next;
}
function mcNum(){
    return mc_objects.length;
}

function setColumnDataType(cidx, dt){
    mc_types[cidx] = dt;
}
function setColumnFilter(cidx, f){
    mc_filters[cidx] = f;
}
function setColumnSource(cidx, s){
    mc_sources[cidx] = s;
}
function fetchColumnData(cidx){
    var dt = mc_types[cidx];
    var s = mc_sources[cidx];
    var f = mc_filters[cidx];
   
    console.log("Fetching:" + dt);
    
    var p = {filters:f,
	     datatype:dt,
	     source:s
	    }

    var column;
    column = cidx;
    $.getJSON("/getsb/fetch",p,function(data){
	setColumn(column,data);
    });
}

function columnOfObject(object){
    var cidx = -1;
    $.each(mc_objects,function(i,item){
	if($.contains(item[0],object[0])){
	    cidx = i;
	    return false;
	};
    });
    return cidx;
}

function setColumn(cidx,data){
    if (cidx){
	cid = c1id;
    } else{
	cid = c0id;
    }

    mc_data[cidx] = data;
    mc_types[cidx] = data[0]['datatype'];

    ue = $("<ul>");
    ue.addClass("column_ul");    
    offsets = []
    ue.append($("<div>").css("height",50));
    les = []
    les.length = data.length

    $.each(data,function(i,item){
	le = $("<li>");
	listlink = $("<a>").attr("href","#");
	listlink.bind('click',{cnum:cidx,i:i},function(event){
	    columnEntryClicked(event.data.cnum,event.data.i);});
	listlink.html(item['tostring']);
	
	try{
	    color =item['locations'].length ==2 ? '#00FF00' : '#0000FF';
	}catch(err){
	    color = '#000000';
	}

	listlink.css('color',color);
	le.append(listlink);
	les[i] = le;
	ue.append(le);
	
    });

    $(cid).children().remove();
    $(cid).append(ue);

    $.each(les,function(i,le){
	mc_offsets[cidx][i] = le[0].offsetTop;
    });
    
    makeAndStyleColumnControls(cidx);
    refreshScrolls();		

    

}



function columnEntryClicked(cnum,cidx){


    d = mc_data[cnum][cidx]
    dtype = mc_types[cnum]
    clickaction = mc_clickactions[cnum];
    
    console.log("CONSOLE DATATYPE:", dtype);
    switch(dtype){
    case 'album':
	console.log( 'switching album' );
	trg = mcNext(cnum);
	mbid = d['album_mbid'];
	setColumnFilter(trg,{album_mbid:mbid});
	setColumnSource(trg,'remote');
	setColumnDataType(trg,'track');
	fetchColumnData(trg);	    
	break;	
	
    case 'artist':
	console.log("YOUCLICKARTIST");
	switch(clickaction){
	case 'members':
	    break;
	    
	case 'albums':
	    trg = mcNext(cnum);
	    mbid = d['artist_mbid'];
	    setColumnFilter(trg,{artist_mbid:mbid});
	    setColumnSource(trg,'remote');
	    setColumnDataType(trg,'album');
	    fetchColumnData(trg);	    
	    break;

	default:
	    console.log("unhandled artist clickaction: " + clickaction);
	}
	break;
    default:
	console.log("clicks on column type: " + dtype + " not yet handled");
    }
    

}

function iScrolled(scrollxy, scrolled_id){
    dy =scrollxy[1];

    which_mc = mc_scroll_ids.indexOf(scrolled_id);
    offsets = mc_offsets[which_mc];
    l = offsets.length;

    idx = 0;
    $.each(offsets,function(i,item){
	if (item > -1* dy){
	    return false;
	} 
	idx += 1;
    });

    
    setHUD(mc_data[which_mc][idx]['tostring']);
    
}