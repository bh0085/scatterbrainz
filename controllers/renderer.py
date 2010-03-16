def minsec(sec):
    return "%d:%02d" % (sec / 60, sec % 60)

def path(track):
    return track.filepath

def artist(track):
    return track.id3artist
    
def title(track):
    return track.id3title

def album(track):
    return track.id3album

def tracknum(track):
    if track.id3tracknum:
        return int(track.id3tracknum.split('/')[0])
    else:
        return ''

def length(track):
    return minsec(track.mp3length)

def bitrate(track):
    return track.mp3bitrate / 1000
