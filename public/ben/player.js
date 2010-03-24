function showPauseBtn()
{
    $("#play").fadeOut(function(){
	$("#pause").fadeIn();
    });
}

function showPlayBtn()
{
    $("#pause").fadeOut(function(){
	$("#play").fadeIn();
    });
}

function playTrack(t,n)
{
    $("#jquery_jplayer").jPlayer("setFile", t).jPlayer("play");
    
    showPauseBtn();
    
    $("#trackname").fadeOut(function(){
	$("#trackname").text(n);
	$("#trackname").fadeIn();
    });
    
    $("#pcent").fadeOut(function(){
	$("#pcent").fadeIn();
    });
    
    return false;
}



$(document).ready(function(){
    
    $("#jquery_jplayer").jPlayer({
	ready: function () {
	}
    })
	.jPlayer("onProgressChange", function(lp,ppr,ppa,pt,tt) {
 	    $("#pcent").text(parseInt(ppa)+"%");
	});
    
    
    $("#pause").hide();
    

    $('a[name|=trklisting]').click(function() {
	console.log($(this).text())
	return(playTrack($(this).title(),$(this).text()  ));
    });
    

    $("#theseparation").click(function() {
 	return(playTrack("http://www.miaowmusic.com/mp3/Miaow-05-The-separation.mp3",$("#theseparation").text()));
    });
    
    $("#lismore").click(function() {
	return(playTrack("http://www.miaowmusic.com/mp3/Miaow-04-Lismore.mp3",$("#lismore").text()));
    });
    
    $("#thinice").click(function() {
	return(playTrack("http://www.miaowmusic.com/mp3/Miaow-10-Thin-ice.mp3",$("#thinice").text()));
    });
    
    $("#play").click(function() {
	$("#jquery_jplayer").jPlayer("play");
	showPauseBtn();
	return false;
    });
    
    $("#pause").click(function() {
	$("#jquery_jplayer").jPlayer("pause");
	showPlayBtn();
	return false;
    });
    
    $("#stop").click(function() {
	$("#jquery_jplayer").jPlayer("stop");
	showPlayBtn();
	return false;
    });
    
    $("#vmax").click(function() {
	$("#jquery_jplayer").jPlayer("volume", 100);
	return false;
    });
    
    $("#vmute").click(function() {
	$("#jquery_jplayer").jPlayer("volume", 0);
	return false;
    });
    
    $("#vhalf").click(function() {
	$("#jquery_jplayer").jPlayer("volume", 50);
	return false;
    });
    
});


