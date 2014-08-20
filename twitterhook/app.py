
import twitter
import collections
# import json

from twitterhook import config
from flask import Flask, jsonify

class TwitterQuery:
    WATCHED_TAG = "#ucphotos"
    def __init__(self):
        self.twitter = twitter.Twitter(auth=twitter.OAuth(
            config.ACCESS_TOKEN,
            config.ACCESS_SECRET,
            config.API_KEY,
            config.API_SECRET))

    def get_photos(self):
        resp = self.twitter.search.tweets(q=self.WATCHED_TAG)

        print("Getting photos. Resp: {}".format(resp))

        media = []
        try:
            for status in resp['statuses']:
                print("Building for status: {}".format(status))
                el = self._build_media(status)
                if el:
                    media.append(el)

        except KeyError:
            media = []

        return media

    def _build_media(self, status):
        this_media = []
        ret = []

        try:
            this_media = status['entities']['media']
        except KeyError:
            return None

        print("Media for status: {}".format(this_media))

        for media in this_media:
            # grab the large version of the image
            ret.append("{}:{}".format(media['media_url_https'], "large"))

        return {"text": status['text'], "images": ret}



twitter = TwitterQuery()
app = Flask(__name__)

@app.route("/new_photos")
def new_photos():
    resp = twitter.get_photos()
    print("Resp: {}".format(resp))
    # resp_json = json.dump(resp)
    return jsonify(results=resp)
