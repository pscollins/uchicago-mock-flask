import argparse
import json

from flask_frozen import Freezer

from mockchicago.app import app, db
from mockchicago.models import Member
from twitterhook.app import app as twitter_app
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
# from mockchicago import views

TWITTER_APP_PORT = 8001

class BadCommandError(Exception):
    pass

def init_db(json_file):
    people = json.load(json_file)

    db.create_all()

    for person in people:
        print("Adding: {}".format(person))
        new_person = Member(**person)
        db.session.add(new_person)

    db.session.commit()


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser("Interact with the server.")
    arg_parser.add_argument(
        "action",
        metavar="action",
        nargs=1,
        help="(run), (init)alize from file, or (gen)erate.")
    arg_parser.add_argument(
        "-f",
        dest="init_file",
        default=None,
        help=("Supply a JSON-formatted configuration file"
              "to initialize the database."))

    args = arg_parser.parse_args()

    print("Got args: {}, action {}".format(args, args.action))
    print("action eq? {}".format(args.action == "init"))

    action = args.action[0]

    if action == "run":
        app.run(debug=True, host="0.0.0.0", port=8000)
    elif action == "freeze":
        freezer = Freezer(app)
        freezer.freeze()
        print("Completed. Check the build/ directory.")
    elif action == "init":
        if args.init_file is not None:
            init_db(open(args.init_file))
        else:
            raise BadCommandError()
    elif action == "clean":
        db.drop_all()
    elif action == "twitter":
        # twitter_app.run(host="0.0.0.0", port=TWITTER_APP_PORT, debug=True)
        twitter_server = HTTPServer(WSGIContainer(twitter_app))
        twitter_server.listen(TWITTER_APP_PORT)
        IOLoop.instance().start()
    else:
        raise BadCommandError()
