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
            var droptarget = event.originalEvent.target;
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
                    $("#playlistbody").append(insertText);
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
            node.draggable({ opacity: 0.7,
                helper: function(event) {
                    return $('<div>').text('o hai');
                },
                appendTo: '#playlistbody'
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
