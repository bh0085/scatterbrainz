function initMainControls(){
    makeControls();
}




var bnames = ['artist','album','track'];
function makeControls(){

    bcm = $("#browseControlsMain");
    nb = bnames.length

    for (i = 0; i < nb ; i++){
	var name = bnames[i];
	var but_id = name+"_button";
	var icon_src = "/icons2/"+name+"Button-med.png"
	var but = $("<a>");
	but.addClass("button");
	but.addClass("browser_control_button");
	but.attr("href","#");
	but.attr("id",but_id);
	but[0].dt = name;
	var butimg = $("<img>")
	butimg.attr("src",icon_src);
	but.click(function(){
		      var rcol = rGetGenericTargetColumn();
		      rcol.setDataType(this.dt);
		      rcol.fetchData();
		 });
	but.append(butimg);
	bcm.append(but);
    }
    styleControls();
}

function styleControls(){
    var w = viewWidth();
    var h = viewHeight();
    
    var bcm = $("#browseControlsMain");
    var bids = [];
    var nb = bnames.length;
    var vw = viewWidth();
    var button_width = 64;
    var button_margin = 3;
    var bw = button_width + button_margin*2;
    var bcm_width = bw*nb;
    var bcm_left = vw/2 - bw*nb/2;
    bcm.css("left",bcm_left);
    bcm.css("width",bcm_width);

    for (var i = 0; i < nb ; i++){
	var name = bnames[i];
	var but_id = name+"_button";
	var but = $("#"+but_id);
	but.css("margin",button_margin);
	but.css("width",button_width);
    }
    

    

}

