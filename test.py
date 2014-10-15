from snapchat import Snapchat

snapchat = Snapchat('snapbot_test', 'snapbot123')

snaps = snapchat.getSnaps()
print snaps[0]['id']
test = snapchat.getMedia(snaps[0]['id'])
with open('/home/projectserver/test.jpg', 'wb') as f:
    f.write(test)
