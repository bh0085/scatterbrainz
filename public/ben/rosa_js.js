function sbmbArtistInfo(data)
{
    console.log(data)
    ue=$("<ul>")
    le=$("<li>");
    //le.html(data[0][0]);//+item['year']);
    ue.append(le);    
    //ue.html(data[0][0]);
    $.each(data,function(i,item){
	le=$("<li>");
	le.html(item[0]);//+item['year']);
	ue.append(le);
    });
    $("#art_output").append(ue);
}

