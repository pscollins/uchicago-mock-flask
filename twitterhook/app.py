import twitter
import collections
import itertools

from twitterhook import config
from flask import Flask
from flask.ext.jsonpify import jsonify

def grouper(n, iterable):
    it = iter(iterable)
    while True:
       chunk = tuple(itertools.islice(it, n))
       if not chunk:
           return
       yield chunk

class TwitterQuery:
    WATCHED_TAG = "#ucphotos"
    PHOTO_FMT = '''<div class="col-md-3">
    <a href="{photo_url}"
    title="{photo_title}"
    data-lightbox-gallery="gallery1">
    <img src="{photo_url}" class="img-responsive" alt="img"></img>
    </a>
    </div>'''
    ROW_FMT = '''<div class="row"> {} </div>'''
    PER_ROW = 4
    MAX_COUNT = 20
    def __init__(self):
        self.twitter = twitter.Twitter(auth=twitter.OAuth(
            config.ACCESS_TOKEN,
            config.ACCESS_SECRET,
            config.API_KEY,
            config.API_SECRET))

    def get_photos(self):
        # resp = self.twitter.search.tweets(
        #     q=self.WATCHED_TAG, count=self.MAX_COUNT)
        resp = self.twitter.statuses.mentions_timeline()

        print("Getting photos. Resp: {}".format(resp))

        media = []
        try:
            for status in resp:
                print("Building for status: {}".format(status))
                el = self._build_media(status)
                if el:
                    media.append(el)

        except KeyError:
            media = []

        return media

    def get_photos_html(self):
        elements = self.get_photos()
        resp = []

        for element in elements:
            text = element['text']
            for image in element['images']:
                resp.append(self.PHOTO_FMT.format(
                    photo_url=image, photo_title=text.replace("\n", " ")))

        wrapped_rows = [self.ROW_FMT.format("\n".join(group))
                        for group in grouper(self.PER_ROW,
                                             resp)]

        return "\n".join(wrapped_rows)

    def _build_media(self, status):
        this_media = []
        ret = []

        try:
            this_media = status['entities']['media']
        except KeyError:
            return None

        print("Media for status: {}".format(this_media))

        for media in this_media:
            # using the large version breaks things, don't know why
            ret.append("{}".format(media['media_url_https']))

        return {"text": status['text'], "images": ret}



twitter = TwitterQuery()
app = Flask(__name__)

@app.route("/new_photos")
def new_photos():
    resp = twitter.get_photos()
    print("Resp: {}".format(resp))
    # resp_json = json.dump(resp)
    return jsonify(results=resp)

@app.route("/new_photos_html")
def new_photos_html():
    resp = twitter.get_photos_html()
    print("Resp: {}".format(resp))

    return jsonify(html=resp)
