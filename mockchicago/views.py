from flask import request, render_template

from mockchicago.app import app
from mockchicago.models import Member, Photo

REMOTE_URL="//ucmocktrial.me"

@app.route("/")
def index():
    all_officers = Member.query.order_by(
        Member.officer_rank.desc()).limit(5).all()

    # president, officer_members = all_officers[0], all_officers[1:]
    officer_members = all_officers

    print("Got officers: {}".format(officer_members))

    photos = Photo.query.all()

    print("Got photos: {}".format(photos))

    return render_template("index.html", president=None,
                           officer_members=officer_members,
                           members_with_modals=officer_members,
                           photos=photos,
                           remote_url=REMOTE_URL)

# for f in glob.glob("*.jpg"):
#     print("f: {}".format(f))
#     photo = Photo(f, "Test title: {}".format(f))
#     db.session.add(photo)
#     print("added photo: {}".format(photo))
