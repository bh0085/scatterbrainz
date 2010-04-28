$(document).ready(function(){

    /**
        * tablesorter and jquery UI sortable BS
        */

    $('#playlist').tablesorter();
    $('#playlistbody').sortable({ axis: 'y', opacity: 0.6,
        containment: 'parent',
        items: 'tr',
        placeholder: 'placeholder',
        distance: 15
    });
    $(".jp-playlist").droppable({
        drop: function(event, ui) {
            var browsenode = ui.draggable;
            if (browsenode.hasClass('browsenode')) {
                addToPlaylist(browsenode.attr('id'), event.originalEvent.target);
            } else {
                return;
            }
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
                    image: '/icons/artist.gif'
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
                },
                distance: 15
            });
        }
    });

    /**
     * jplayer playlist BS
     */
    
    var global_lp = 0;
    $("#jquery_jplayer")
    .jPlayer( {
        ready: function () {
            $('.song').live('dblclick', play);
        }
    })
    .jPlayer("onSoundComplete", playListNext)
    .jPlayer("onProgressChange", function(lp,ppr,ppa,pt,tt) {
	    var lpInt = parseInt(lp);
	    var ppaInt = parseInt(ppa);
	    global_lp = lpInt;

	    $('#loaderBar').progressbar('option', 'value', lpInt);
	    $('#sliderPlayback').slider('option', 'value', ppaInt);
	    
	    //jpPlayTime.text($.jPlayer.convertTime(playedTime));
	    //jpTotalTime.text($.jPlayer.convertTime(totalTime));
    });
    
    $("#prev").click(playListPrev);
    $("#next").click(playListNext);
    $("#play").click(function() {
	$('#play').hide();
	$('#pause').show();
	$("#jquery_jplayer").jPlayer("play");
    });
    $("#pause").click(function() {
	$('#play').show();
	$('#pause').hide();
	$("#jquery_jplayer").jPlayer("pause");
    });

    $("#volume-min").click( function() {
	    $('#jquery_jplayer').data("jPlayer.config").audio.muted = false;
	    $("#volume-max").toggle();
	    $("#volume-min").toggle();
    });

    $("#volume-max").click( function() {
	    $('#jquery_jplayer').data("jPlayer.config").audio.muted = true;
	    $("#volume-max").toggle();
	    $("#volume-min").toggle();
    });

    $("#player_progress_ctrl_bar a").live( "click", function() {
	    $("#jquery_jplayer").jPlayer("playHead", this.id.substring(3)*(100.0/global_lp));
	    return false;
    });

    // Slider
    $('#sliderPlayback').slider({
	    max: 100,
	    range: 'min',
	    animate: true,

	    slide: function(event, ui)
    {
	    $("#jquery_jplayer").jPlayer("playHead", ui.value*(100.0/global_lp));
    }
    });

    $('#sliderVolume').slider({
	    value : 80,
	    max: 100,
	    range: 'min',
	    animate: true,

	    slide: function(event, ui)
    {
	    $("#jquery_jplayer").jPlayer("volume", ui.value);
    }
    });

    $('#loaderBar').progressbar();


    //hover states on the static widgets
    $('#dialog_link, ul#icons li').hover(
	    function() { $(this).addClass('ui-state-hover'); },
	    function() { $(this).removeClass('ui-state-hover'); }
    );

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
                $('.lastSelected').removeClass('lastSelected');
                self.addClass('selected').addClass('lastSelected');
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
        var next = $('.selected:last').next('tr');
        var prev = $('.selected:first').prev('tr');
        $('.selected').remove();
        if (next.length) {
            next.addClass('selected').addClass('lastSelected');
        } else if (prev.length) {
            prev.addClass('selected').addClass('lastSelected');
        }
        return false;
    });

    $('.jp-playlist').bind('keydown', 'down', function() {

        var next = $('.lastSelected').next();
        if (next.length > 0) {
            $('.selected').removeClass('selected').removeClass('lastSelected');
           next.addClass('selected').addClass('lastSelected');
          scrollTo(next, $('.jp-playlist'));
        }

        return false;
    });

    $('.jp-playlist').bind('keydown', 'up', function() {
        var prev = $('.lastSelected').prev();
        if (prev.length > 0) {
            $('.selected').removeClass('selected').removeClass('lastSelected');
            prev.addClass('selected').addClass('lastSelected');
            scrollTo(prev, $('.jp-playlist'));
        }
        return false;
    });

    /**
        * Dispatch clicks to fake floating table header over to real table header
        */
    $('#playlistHeadTable th.artist').click(function() {
        $('#playlist th.artist').click();
    });
    $('#playlistHeadTable th.title').click(function() {
        $('#playlist th.title').click();
    });
    $('#playlistHeadTable th.album').click(function() {
        $('#playlist th.album').click();
    });
    $('#playlistHeadTable th.tracknum').click(function() {
        $('#playlist th.tracknum').click();
    });
    $('#playlistHeadTable th.length').click(function() {
        $('#playlist th.length').click();
    });
    $('#playlistHeadTable th.bitrate').click(function() {
        $('#playlist th.bitrate').click();
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

    $('#ditchSearch').click(ditchSearch)
                     .button({
                        icons: {
                            primary: 'ui-icon-circle-close'
                        },
                        text: false
                     });

    $('#goSearch').click(searchHandler)
                     .button({
                        icons: {
                            primary: 'ui-icon-circle-triangle-e'
                        },
                        text: false
                     });

    $(window).resize(windowResize);
    
    $("#playMode").buttonset();

    setTimeout(function() {
        $("body").splitter({
            'sizeLeft' : true,
            'cursor'   : 'col-resize',
            'resizeToWidth' : true
        });
        $(".vsplitbar").addClass('expandHeightToFitBrowser')
                        .attr('expandHeightOffsetPx', 75);
        $(window).resize();
    }, 100);
});

function windowResize(target) {
    $(document).data('windowHeightPx', $(window).height());
    $(document).data('windowWidthPx', $(window).width());
    var elements = $(".expandHeightToFitBrowser");
    for (var i=0; i<elements.length; i++) {
        expandHeightToFitBrowser($(elements[i]));
    }
}

function expandHeightToFitBrowser(element) {
    var elementTopPx = element.offset().top;
    var elementOffsetPx = element.attr('expandHeightOffsetPx');
    var elementHeightPx = $(document).data('windowHeightPx') - elementTopPx - elementOffsetPx;
    element.height(elementHeightPx);
}

function scrollTo(e, c) {

    if (!e) {
        return;
    }

    var eTop = e.offset().top;
    var eBottom = eTop + e.height();
    var cTop = c.offset().top;
    var cBottom = cTop + c.height();

    if ((eBottom > cBottom) || (eTop < cTop)) {
        if (eBottom > cBottom) {
            var scrollTop = c.attr('scrollTop') + (eBottom - cBottom) + 'px';
        } else if (eTop < cTop) {
            var scrollTop = c.attr('scrollTop') - (cTop - eTop) + 'px';
        }
        c.stop();
        c.animate({scrollTop: scrollTop}, 100);
    }

}

function scrollToBottom(c) {
    c.animate({scrollTop: c.attr('scrollHeight') + 'px'}, 500);
}

function scrollToTop(c) {
    c.animate({scrollTop: '0px'}, 500);
}

function addToPlaylist(id, target) {
    $(document).data('playlistDropTarget', target);
    $.getJSON(
        '/hello/getTracksAJAX',
        {'id': id},
        addToPlaylistCallback
    );
}

function addToPlaylistCallback(data) {
    var insertText = '';
    $.each(data, function(count, trackJSON) {
        insertText += '<tr id="track_'+trackJSON['id']+'" class="song" href="'
                                                      +trackJSON['filepath']+'">'
            + '<td class="artist">'+trackJSON['artist']+'</td>'
            + '<td class="title">'+trackJSON['title']+'</td>'
            + '<td class="album">'+trackJSON['album']+'</td>'
            + '<td class="tracknum">'+trackJSON['tracknum']+'</td>'
            + '<td class="length">'+trackJSON['length']+'</td>'
            + '<td class="bitrate">'+trackJSON['bitrate']+'</td>'
        + '</tr>';
    });
    var dropTarget = $(document).data('playlistDropTarget');
    if (dropTarget && dropTarget.tagName == 'TD') {
        $(dropTarget).parent().after(insertText);
    } else {
        $("#playlistbody").append(insertText);
    }
    $('#playlist thead th').unbind('click');
    $('#playlist').tablesorter();
}

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
    $('#browser').hide();
    $('#searchBrowser').show();
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
    setDocumentTitle($('.artist', row).text() + ' - ' +
                     $('.title', row).text());
    populatePlayingTrackInfo(row.attr('id'));
    $('#play').hide();
    $('#pause').show();
}

function setDocumentTitle(title) {
    document.title = title;
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
            } else if ($('#playlistRepeat').attr('checked')) {
                $('.song:first').dblclick();
            } else if ($('#playlistRandomTrack').attr('checked')) {
                nextRandomTrack();
            } else if ($('#playlistRandomAlbum').attr('checked')) {
                nextRandomAlbum();
            } else {
		$('#play').show();
		$('#pause').hide();
	    }
        } else {
            if (playing.prev().hasClass('song')) {
                playing.prev().addClass('playing');
                playRow(playing.prev());
            } else {
		$('#play').show();
		$('#pause').hide();
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

function nextRandomTrack() {
    $.getJSON(
        '/hello/randomTrackAJAX',
        {},
        playRandomCallback
    );
}

function nextRandomAlbum() {
    $.getJSON(
        '/hello/randomAlbumAJAX',
        {},
        playRandomCallback
    );
}

function playRandomCallback(data) {
    var last = $('.song:last');
    $(document).data('playlistDropTarget', null);
    addToPlaylistCallback(data);
    last.next('.song').dblclick();
}

function populatePlayingTrackInfo(trackid) {
    $.getJSON(
        '/hello/getPlayingTrackInfoAJAX',
        {'trackid': trackid},
        function(data) {
            if ('albumArtURL' in data) {
                $('#albumArt').attr('src', data['albumArtURL']);
		$('#albumArt').show();
		$('#noAlbumArt').hide();
            } else {
                $('#albumArt').hide();
		$('#noAlbumArt').show();
            }
            $('#playingArtist').html(data['artist']);
            $('#playingAlbum').html(data['album']);
            $('#playingTrack').html(data['track']);
        }
    );
}
