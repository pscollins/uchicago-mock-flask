from app import db

class Member(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    first_name = db.column(db.String(100))
    last_name = db.column(db.String(100))
    email = db.column(db.String(100))

    officer_rank = db.column(db.Integer)
    bio_msg = db.column(db.String(50000))
    img_name = db.column(db.String(300))

    def __init__(self, first_name, last_name,
                 email="", officer_rank=-1, bio_msg=""):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.officer_rank = officer_rank
        self.bio_msg = bio_msg
