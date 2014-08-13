from mockchicago.app import db

class Member(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    officer_rank = db.Column(db.Integer)
    bio_msg = db.Column(db.String(50000))
    img_name = db.Column(db.String(300))

    # we're going to have low-rank mean regular person (-1 == no
    # special role), then ascending order to the top. social chairs ==
    # 1, webmaster == 2, td == 3, asst vp travel == 4, admin == 5,
    # finance == 6, travel == 7, pres == 8
    def __init__(self, first_name, last_name,
                 email="", officer_rank=-1, bio_msg="",
                 img_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.officer_rank = officer_rank
        self.bio_msg = bio_msg
        self.img_name = img_name

    def title(self):
        return {
            8: "President",
            7: "VP Travel",
            6: "VP Finance",
            5: "VP Admin",
            4: "Assistant VP Travel",
            3: "Tournament Director",
            2: "Webmaster",
            1: "Social Chair",
            -1: None
        }[self.officer_rank]

    def img_path(self):
        PATH_FMT = "/static/img/member_photos/{}"
        DEFAULT_IMG_NAME = "default-user.png"

        return PATH_FMT.format(self.img_name or DEFAULT_IMG_NAME)
        # return PATH_FMT.format(DEFAULT_IMG_NAME)

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def msg_with_email(self):
        return "{} {}.".format(self.bio_msg, self.email)


class Photo(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    img_name = db.Column(db.String(100))
    title = db.Column(db.String(200))

    def __init__(self, img_name, title):
        self.img_name = img_name
        self.title = title

    def img_path(self):
        PATH_FMT = "/static/img/general_photos/{}"

        return PATH_FMT.format(self.img_name)
