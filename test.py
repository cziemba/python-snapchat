from snapchat import Snapchat
from os.path import expanduser
import time
from pprint import pprint

snapchat = Snapchat('user', 'pass')

#pprint(update)
snap_id_cache = []

while True:
    snaps = [s for s in snapchat.getSnaps() if s['id'] not in snap_id_cache]
    print "got {} snaps!".format(len(snaps))
    for snap in snaps:
        print snap['id']
        snap_id_cache.append(snap['id'])

        data = snapchat.getMedia(snap['id'])
        if data is not None:
            with open(expanduser('~') + '/' + snap['id'] + '.jpg', 'wb') as f:
                f.write(data)

        snapchat.markSnapViewed(snap['id'], 30)
    if len(snaps) > 0:
        snapchat.clearFeed()
    time.sleep(10)
