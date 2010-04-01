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
        $('.selected').remove();
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

    $('#ditchSearch').click(ditchSearch);

    $('#goSearch').click(searchHandler);

    $(window).resize(windowResize);

    setTimeout(function() {
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
    //var elements = $(".expandWidthToFitBrowser");
    //for (var i=0; i<elements.length; i++) {
        //expandWidthToFitBrowser($(elements[i]));
    //}
}

function expandHeightToFitBrowser(element) {
    var elementTopPx = element.offset().top;
    var elementOffsetPx = element.attr('expandHeightOffsetPx');
    var elementHeightPx = $(document).data('windowHeightPx') - elementTopPx - elementOffsetPx;
    element.height(elementHeightPx);
}

function scrollTo(e, c) {

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
        function(data) {
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
    );
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
    grabAlbumArt(row.attr('id'));
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

function grabAlbumArt(trackid) {
    $.getJSON(
        '/hello/albumArtAJAX',
        {'trackid': trackid},
        function(data) {
            if ('albumArtURL' in data) {
                $('#albumArt').attr('src', data['albumArtURL']);
                $('#albumArtContainer').show();
            } else {
                $('#albumArtContainer').hide();
            }
        }
    );
}
