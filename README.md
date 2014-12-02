Python Snapchat
===============

I couldn't find a nice working implementation of the snapchat API in python so I decided to port [php-snapchat](https://github.com/JorgenPhi/php-snapchat) into python.

Example
-------
This will read all snapchats and output them as jpgs.

```python
from snapchat import Snapchat

snapchat = Snapchat(snap_user, snap_pass)

snaps = snapchat.getImages() # List of incoming snapchat infos that are images
for snap in snaps:
    data = snapchat.getMedia(snap['id'])
    if data is not None:
        with open(snap['id'] + '.jpg', 'wb' as f:
            f.write(data)
```

TODO
----
- Finish porting some of the more important functionality
- Unit Tests!
- Work on Stories, Account control (friends), and Video (eventually)

LICENSE
-------
MIT
