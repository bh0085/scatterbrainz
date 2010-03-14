$(document).ready(function(){

    /**
     * tablesorter and jquery UI sortable BS
     */
    
    $('#playlist').tablesorter();
    $('#playlistbody').sortable({ axis: 'y', opacity: 0.6,
                                  containment: 'parent', items: 'tr',
                                  placeholder: 'placeholder'});
    $('#browser').tree({
	data : { 
	    async : true,
	    type : 'json',
	    opts : {
		    url : '/hello/treebrowse'
	    }
	},
	ui : {
	    theme_name : 'default'
	},
	plugins : {
	    hotkeys : { }
	}
    });
    
    /**
     * jplayer playlist BS
     */
    
    $("#jquery_jplayer").jPlayer( {
        ready: function () {
            $('.song').dblclick(play);
        }
    });
    var jpPlayTime = $("#jplayer_play_time");
    var jpTotalTime = $("#jplayer_total_time");
    $("#jquery_jplayer").jPlayer("onProgressChange",
    function(loadPercent, playedPercentRelative,
             playedPercentAbsolute, playedTime, totalTime) {
        jpPlayTime.text($.jPlayer.convertTime(playedTime));
        jpTotalTime.text($.jPlayer.convertTime(totalTime));
    }).jPlayer("onSoundComplete", playListNext);
    $("#jplayer_previous").click(playListPrev);
    $("#jplayer_next").click(playListNext);

});

function playRow(row) {
    $('.playing').removeClass('playing');
    $("#jquery_jplayer").jPlayer("setFile", row.attr('href'))
                        .jPlayer("play");
    row.addClass('playing');
}

function stop() {
    $("#jquery_jplayer").jPlayer("stop");
}
                              
function play() {
    playRow($(this));
}

function playlistNextPrev(next) {
    var playing = $('.playing');
    if (playing) {
        playing.removeClass('playing');
        if (next) {
            if (playing.next().hasClass('song')) {
                playing.next().addClass('playing');
                playRow(playing.next());
            } else {
                stop();
            }
        } else {
            if (playing.prev().hasClass('song')) {
                playing.prev().addClass('playing');
                playRow(playing.prev());
            } else {
                stop();
            }
        }
    }
}

function playListPrev() {
    playlistNextPrev(false);
}

function playListNext() {
    playlistNextPrev(true);
}

/**
 * Playlist rendering stuff
 */
function playlistRowMap(trackJSON) {
    
}
