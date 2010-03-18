


$(document).ready(function(){

    $('#player').click(function(event){
     alert("Thanks for visiting!");
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

 

});
