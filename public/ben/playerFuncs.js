function playerShowTracks(data)
{
    var tldiv = "#tracklist";
    ue=$("<ul>");
    $.each(data,function(i,item){
	le = $("<li>")
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

  
    $('a[name|=trklisting]').click(function() {
	    return(playTrack($(this).attr('title'),$(this).text()  ));
    });
}