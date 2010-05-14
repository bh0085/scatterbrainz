function playerShowTracks(data)
{
    var tldiv = "#tracklist";
    ue=$("<ul>");
    $.each(data,function(i,item){
	le = $("<li>")
	l0 =$("<a>");
	l0.addClass("displayrelations")
	l0.addClass("trackextra")
	l0.attr("href","#");
	l0.attr("name",item['id']);
	l0.html("REL ");
	le.append(l0);

	l1 =$("<a>");
	l1.addClass("displaymembers")
	l1.addClass("trackextra")
	l1.attr("href","#");
	l1.attr("name",item['id']);
	l1.html("BAND ");
	le.append(l1);

	link=$("<a>");
	br = $("<br>");
	link.attr("name",'trklisting');
	link.attr("id",item['id']);
	link.html(item["name"])
	link.attr("title",item['url']);
	link.attr("href","#");
	link.append(br)
	le.append(link)
	ue.append(le)
	
    });
    
    $(tldiv).append(ue)

    //newdiv=$(tldiv).makeacolumnlists({cols: 3, colWidth: 0, equalHeight: 'li', startN: 1});
    $(tldiv).columnize({width:250})

    $('.displayrelations').click(function(){
	$.getJSON("/getlocal/trackRelationsMB",{trackid:$(this).attr("name")},playerShowTrackRelations);
    });
    $('.displaymembers').click(function(){
	$.getJSON("/getmb/currentMembersForTrackArtist",{trackid:$(this).attr("name")},playerShowBandMembers);
    });

    $('a[name|=trklisting]').click(function() {
	$.getJSON("/getlocal/trackArtistAlbumsLOCAL",{trackid:$(this).attr("id")},playerShowRelatedAlbums);	
	$.getJSON("/getlocal/trackArtistAlbumsMB",{trackid:$(this).attr("id")},playerShowRelatedMB);
	return(playTrack($(this).attr('title'),$(this).text()  ));
    });
}
function playerShowRelatedAlbums(data){
    ue=$("<ul>");
    $.each(data,function(i,item){
	le=$("<li>");
	le.html(item['name']+item['year']);
	ue.append(le);
    });
    $("#rel_albums").children().remove();
    $("#rel_albums").append(ue); 

}
function playerShowRelatedMB(data){
    ue=$("<ul>");
    $.each(data,function(i,item){
	le=$("<li>");
	le.html(item['name']);//+item['year']);
	ue.append(le);
    });
    $("#mb_albums").children().remove();
    $("#mb_albums").append(ue); 

}
function playerShowTrackRelations(data){
   
    ue=$("<ul>");

    le=$("<li>");
    le.html("Track Relations:");//+item['year']);
    ue.append(le);    

    $.each(data['track_relations'],function(i,item){
	le=$("<li>");
	le.html(item['type']);//+item['year']);
	ue.append(le);
    });
    $.each(data['artist_relations'],function(i,item){
	le=$("<li>");
	le.html(item['type']);//+item['year']);
	ue.append(le);
    });
    $("#track_relations").children().remove();
    $("#track_relations").append(ue);     
}
function playerShowBandMembers(data){
    ue=$("<ul>")

    le=$("<li>");
    le.html("Current Members");//+item['year']);
    ue.append(le);    

    $.each(data['current_members'],function(i,item){
	le=$("<li>");
	le.html(item);//+item['year']);
	ue.append(le);
    });

    le=$("<li>");
    le.html("Past Members");//+item['year']);
    ue.append(le);    

    $.each(data['past_members'],function(i,item){
	le=$("<li>");
	le.html(item);//+item['year']);
	ue.append(le);
    });

    $("#track_relations").children().remove();
    $("#track_relations").append(ue);         
}