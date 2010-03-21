$(document).ready(function(){

    /**
     * tablesorter and jquery UI sortable BS
     */

    $('#playlist').tablesorter();
    $('#playlistbody').sortable({ axis: 'y', opacity: 0.6,
        containment: 'parent',
        items: 'tr',
        placeholder: 'placeholder'
    });
    $("#playlistbody").droppable({
        drop: function(event, ui) {
            var browsenode = ui.draggable;
	    if (!browsenode.hasClass('browsenode')) {
		return;
	    }
            $(document).data('playlistDropTarget', event.originalEvent.target);
            $.getJSON(
                '/hello/getTracksAJAX',
                {'id':browsenode.attr('id')},
                function(data) {
                    var insertText = '';
                    $.each(data, function(count, trackJSON) {
                        insertText += '<tr class="song" href="'+trackJSON['filepath']+'">'
                                      + '<td class="artist">'+trackJSON['artist']+'</td>'
                                      + '<td class="title">'+trackJSON['title']+'</td>'
                                      + '<td class="album">'+trackJSON['album']+'</td>'
                                      + '<td class="tracknum">'+trackJSON['tracknum']+'</td>'
                                      + '<td class="length">'+trackJSON['length']+'</td>'
                                      + '<td class="bitrate">'+trackJSON['bitrate']+'</td>'
                                    + '</tr>';
                    });
                    var dropTarget = $(document).data('playlistDropTarget');
                    if (dropTarget.tagName == 'TD') {
                        $(dropTarget).parent().after(insertText);
                    } else {
                        $("#playlistbody").append(insertText);
                    }
                    $('#playlist thead th').unbind('click');
                    $('#playlist').tablesorter();
                }
            );
        }
    });
    $('#browser').tree({
        data : { 
            async : true,
            type : 'json',
            opts : {
                url : '/hello/treeBrowseAJAX'
            }
        },
	callback : { 
	    beforedata : function (n, t) {
		return { id : $(n).attr("id") || 'init' };
	    }
	},
        ui : {
            theme_name : 'default'
        },
        plugins : {
            hotkeys : { }
        },
        types : {
            'default' : {
                clickable	: true,
                renameable	: false,
                deletable	: false,
                creatable	: false,
                draggable	: false,
                max_children	: -1,
                max_depth	: -1,
                valid_children	: 'all',
                icon : {
                    image : false,
                    position : false
                }
            },
            'Artist': {
                icon: {
                    image: '/icons/person4small.gif'
                }
            },
            'Album': {
                icon: {
                    image: '/icons/cd2small.gif'
                }
            },
            'Track': {
                icon: {
                    image: '/icons/note2small.jpg'
                }
            }
        }
    });

    /**
     * make browser nodes draggable w/ jquery ui live shit
     */
    $('li.browsenode').live("mouseover", function() {
        node = $(this);
        if (!node.data("init")) {
            node.data("init", true);
            node.draggable({
                opacity: 0.7,
                appendTo: '#playlistbody',
                cursorAt: {left: -1, top: -1},
                helper: function(event) {
                    return $('<span>' + event.target.text + '</span>');
                }
            });
        }
    });

    /**
     * jplayer playlist BS
     */

    $("#jquery_jplayer").jPlayer( {
        ready: function () {
            $('.song').live('dblclick',play);
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
    
    /**
     * Playlist interaction, shift click, ctrl click, del, etc
     */
    $('.song').live('click', function(e) {
	$('.jp-playlist').focus();
	var self = $(this);
	var lastselected = $('.lastSelected');
	if (lastselected.length > 0) {
	    if (e.shiftKey) {
		if (self.prevAll('.lastSelected').length > 0) {
		    self.prevUntil('.lastSelected').addClass('selected');
		} else {
		    self.nextUntil('.lastSelected').addClass('selected');
		}
		self.addClass('selected');
		return true;
	    } else if (e.ctrlKey) {
		self.toggleClass('selected').addClass('lastSelected');
		return true;
	    }
	}
	$('.selected').removeClass('selected');
	$('.lastSelected').removeClass('lastSelected');
	self.addClass('selected').addClass('lastSelected');
	return true;
    });
    
    $('.jp-playlist').bind('keydown', 'ctrl+a', function() {
	$('.song').addClass('selected');
	return false;
    });
    
    $('.jp-playlist').bind('keydown', 'del', function() {
	$('.selected').remove();
	return false;
    });
    
    /**
     * initialize search
     */
    $('#searchInput').keydown(function(e) {
        if(e.keyCode == 13) {
	    searchHandler();
	} else if (e.keyCode == 27) {
	    ditchSearch();
	}
    });
    
    $('#ditchSearch').click(ditchSearch);
    
    $('#goSearch').click(searchHandler);

});

function searchHandler() {
    var searchStr = $('#searchInput').attr('value').trim();
    if (searchStr == "") {
	ditchSearch();
    } else {
	search(searchStr);
    }
}

function search(searchStr) {
    $.getJSON(
	'/hello/searchAJAX',
	{'search' : searchStr},
	searchCallback
    );
}

function searchCallback(results) {
    $('#searchBrowser').tree({
        data : {
	    async : true,
            type : 'json',
            opts : {
		url : '/hello/treeBrowseAJAX'
	    }
        },
	callback : { 
	    // Make sure static is not used once the tree has loaded for the first time
	    onload : function (t) { 
		t.settings.data.opts.static = false; 
	    },
	    // Take care of refresh calls - n will be false only when the whole tree is refreshed or loaded of the first time
	    beforedata : function (n, t) {
		if(n == false) t.settings.data.opts.static = results;
		return { id : $(n).attr("id") || 'init' };
	    }
	},
        ui : {
            theme_name : 'default'
        },
        plugins : {
            hotkeys : { }
        },
        types : {
            'default' : {
                clickable	: true,
                renameable	: false,
                deletable	: false,
                creatable	: false,
                draggable	: false,
                max_children	: -1,
                max_depth	: -1,
                valid_children	: 'all',
                icon : {
                    image : false,
                    position : false
                }
            },
            'Artist': {
                icon: {
                    image: '/icons/person4small.gif'
                }
            },
            'Album': {
                icon: {
                    image: '/icons/cd2small.gif'
                }
            },
            'Track': {
                icon: {
                    image: '/icons/note2small.jpg'
                }
            }
        }
    });
    $('#browser').hide();
    $('#searchBrowser').show();
}

function ditchSearch() {
    $('#searchInput').attr('value', '');
    $('#browser').show();
    $('#searchBrowser').hide();
}

String.prototype.trim = function() {
    return this.replace(/^\s+|\s+$/g,"");
}

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
