import time
import json
import random

from snapchat_agent import SnapchatAgent
from snapchat_cache import SnapchatCache
from pprint import pprint


class Snapchat(SnapchatAgent):

    #Media Flags
    MEDIA_IMAGE = 0
    MEDIA_VIDEO = 1
    MEDIA_VIDEO_NOAUDIO = 2

    MEDIA_FRIEND_REQUEST = 3

    MEDIA_FRIEND_REQUEST_IMAGE = 4
    MEDIA_FRIEND_REQUEST_VIDEO = 5
    MEDIA_FRIEND_REQUEST_VIDEO_NOAUDIO = 6

    STATUS_NONE = -1
    STATUS_SENT = 0
    STATUS_DELIVERED = 1
    STATUS_OPENED = 2
    STATUS_SCREENSHOT = 3

    FRIEND_CONFIRMED = 0
    FRIEND_UNCONFIRMED = 1
    FRIEND_BLOCKED = 2
    FRIEND_DELETED = 3

    PRIVACY_EVERYONE = 0
    PRIVACY_FRIENDS = 1

    def __init__(self, username=None, password=None, auth_token=None):
        super(Snapchat, self).__init__()
        self.auth_token = None
        self.username = None

        if password is not None:
            if self.login(username, password) is False:
                raise Exception("Login Failure")
        elif auth_token is not None:
            self.auth_token = auth_token
            self.username = username
            self.cache = SnapchatCache()

    def _empty(self, dictionary, key):
        if key in dictionary:
            return False
        return True

    def login(self, username, password):
        timestamp = super(Snapchat, self).timestamp()
        result = super(Snapchat, self).post(
            '/login',
            [
                ('username', username),
                ('password', password),
                ('timestamp', str(timestamp))
            ],
            [
                super(Snapchat, self).STATIC_TOKEN,
                str(timestamp)
            ]
        )

        if result is None:
            return False

        if 'logged' in result and result['logged']:
            self.auth_token = result['auth_token']
            self.username = result['username']
            self.cache = SnapchatCache()
            self.cache.set('updates', result)
            return True
        else:
            return False

    def logout(self):
        if self.auth_token is None or self.username is None:
            return False

        timestamp = super(Snapchat, self).timestamp()
        result = super(Snapchat, self).post(
            '/logout',
            [
                ('timestamp', str(timestamp)),
                ('username', self.username)
            ],
            [
                self.auth_token,
                str(timestamp)
            ]
        )
        self.cache = None
        return result is None

    def register(self, username, password, email, birthday):
        #TODO: implement
        return

    def getUpdates(self, force=False):
        if not force:
            result = self.cache.get('updates')
            if result:
                return result

        if self.auth_token is None or self.username is None:
            return None

        timestamp = super(Snapchat, self).timestamp()
        result = super(Snapchat, self).post(
            '/all_updates',
            [
                ('timestamp', str(timestamp)),
                ('username', self.username)
            ],
            [
                self.auth_token,
                str(timestamp)
            ]
        )

        if 'updates_response' in result:
            self.auth_token = result['updates_response']['auth_token']
            self.cache.set('updates', result['updates_response'])
            return result['updates_response']
        return result

    def getSnaps(self):
        updates = self.getUpdates()

        if updates is None:
            return None

        snaps = []
        for snap in updates['snaps']:
            snaps.append({
                'id': snap['id'],
                'media_id': None if self._empty(snap, 'm') else snap['m'],
                'time': None if self._empty(snap, 't') else snap['t'],
                'sender': None if self._empty(snap, 'sn') else snap['sn'],
                'recipient': None if self._empty(snap, 'rp') else snap['rp'],
                'status': snap['st'],
                'screenshot_count': None if self._empty(snap, 'c') else snap['c'],
                'sent': snap['sts'],
                'opened': snap['ts'],
                'broadcast': None if self._empty(snap, 'broadcast') else {
                    'url': snap['broadcast_url'],
                    'action_text': snap['broadcast_action_text'],
                    'hide_timer': snap['broadcast_hide_timer']
                }
            })
        return snaps

    def getImages(self):
        images = [s for s in self.getSnaps() if s['media_id'] == self.MEDIA_IMAGE]
        return images

    def getFriendStories(self, force=False):
        #TODO: Implement
        return

    def findFriends(self, numbers, country='US'):
        #TODO: Implement
        return

    def getFriends(self):
        #TODO: :(
        return

    def getAddedFriends(self):
        #TODO: Implement
        return

    def addFriend(self, username):
        #TODO: Implement
        return

    def addFriends(self, usernames):
        #TODO: Implement
        return

    def deleteFriend(self, username):
        #TODO: Implement
        return

    def setDisplayName(self, username, display):
        #TODO: Implement
        return

    def block(self, username):
        #TODO: Implement
        return

    def unblock(self, username):
        #TODO: Implement
        return

    def getMedia(self, id):
        if self.auth_token is None or self.username is None:
            return None

        timestamp = super(Snapchat, self).timestamp()
        result = super(Snapchat, self).post(
            '/blob',
            [
                ('id', id),
                ('timestamp', str(timestamp)),
                ('username', self.username)
            ],
            [
                self.auth_token,
                str(timestamp)
            ]
        )

        if result is None:
            return None

        if super(Snapchat, self).isMedia(result[:2]):  # not encrypted
            return result
        else:  # must decrypt
            result = super(Snapchat, self).decryptECB(result)

            if super(Snapchat, self).isMedia(result[:2]):
                return result

            if super(Snapchat, self).isCompressed(result[:2]):
                result = super(Snapchat, self).unCompress(result)
                return result
        return None

    def sendEvents(self, events, snap_info=None):
        if self.auth_token is None or self.username is None:
            return False

        timestamp = super(Snapchat, self).timestamp()
        result = super(Snapchat, self).post(
            '/update_snaps',
            [
                ('events', json.dumps(events)),
                ('json', json.dumps(snap_info)),
                ('timestamp', str(timestamp)),
                ('username', self.username)
            ],
            [
                self.auth_token,
                str(timestamp)
            ]
        )
        return result is None

    def markSnapViewed(self, id, time_s=1):
        snap_info = {
            'id': {
                't': str(time.time() * 1000),
                'sv': str(time_s + (random.random() / 10))
            }
        }
        events = [
            {
                'eventName': 'SNAP_VIEW',
                'params': {'id': id},
                'ts': str((time.time() * 1000) - time_s)
            },
            {
                'eventName': 'SNAP_EXPIRED',
                'params': {'id': id},
                'ts': str(time.time() * 1000)
            }
        ]
        return self.sendEvents(events, snap_info)

    def markSnapShot(self, id, time_s=1):
        #TODO: Implement
        return

    def upload(self, type, data):
        #TODO: Implement
        return

    def send(self, media_id, recipients, time_s=3):
        #TODO: Implement
        return

    def setStory(self, media_id, media_type, time_s=3):
        #TODO: Implement
        return

    def getStory(self, media_id, key, iv):
        #TODO: Implement
        return

    def getStoryThumb(self, media_id, key, iv):
        #TODO: Implement
        return

    def markStoryViewed(self, id, screenshot_count=0):
        #TODO: Implement
        return

    def getBests(self, friends):
        #TODO: Implement
        return

    def clearFeed(self):
        """
        Sends clear feed. Returns False on failure.
        :return: bool
        """
        if self.auth_token is None or self.username is None:
            return False

        timestamp = super(Snapchat, self).timestamp()
        result = super(Snapchat, self).post(
            '/clear',
            [
                ('timestamp', str(timestamp)),
                ('username', self.username)
            ],
            [
                self.auth_token,
                str(timestamp)
            ]
        )
        return result is None

    def updatePrivacy(self, setting):
        #TODO: Implement
        return

    def updateEmail(self, email):
        #TODO: Implement
        return
