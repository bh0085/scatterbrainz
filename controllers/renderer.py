def getFullPath(track):
    return '/'.join(track['filepath']) + '/' + track['filename']

def minsec(sec):
    return "%d:%02d" % (sec / 60, sec % 60)

def artist(track):
    return track['id3'].get('artist', '')
    
def title(track):
    return track['id3'].get('title', '')

def album(track):
    return track['id3'].get('album', '')

def tracknum(track):
    if 'tracknumber' in track['id3']:
        return int(track['id3']['tracknumber'].split('/')[0])
    else:
        return ''

def length(track):
    return minsec(track['mp3']['length'])

def bitrate(track):
    return track['mp3']['bitrate'] / 1000
