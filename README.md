uchicago-mock-flask
===================

# Requirements

* Python 3.3+
* Virtualenv
* SQLite3 (building the website only)
* openssl (running the twitter client only --- probably not on your local machine)

If you're on linux, you can grab these through apt-get. If you're on
OS X, you can (probably) grab them through homebrew or macports. You
can get virtualenv via `pip`, too.

Once you've got those installed, run

    virtualenv -p python3 venv

Then

    source venv/bin/activate
	pip3 install -r requirements.txt

**Always run `source venv/bin/activate` before you do anything in a new shell**.

# Overview

The project is split into two parts, which live in the `mockchicago/`
and `twitterhook/` directories, respectively. The `run.py` file is
responsible for kicking off both of them.

## Previewing the site

Once you've got everything installed, you should be able to run the webserver:

    python3 ./run.py run

And navigate to [localhost:8000](localhost:8000) in your favorite
browser to see a preview of the site as it looks now. If you can't,
something has gone wrong.

## Updating the site

All of the site configuration is done by editing JSON. Never edit raw
HTML.

### Making your edits for the new board members

The current configuration should be in
`mockchicago/data/members.json`. For each board member, we want to
make the following object:

	{
		"first_name": "John",
		"last_name": "Doe",
		"email": "jdoe@uchicago.edu",
		"officer_rank": N,
		"bio_msg": "fgsfds",
		"img_name": "board_jd.jpg"
	},

`"officer rank"` is an integer between 8 and -1 indicating the role of
the person. Roles are as follows:

* 8 -> President
* 7 -> Travel
* 6 -> Finance
* 5 -> Admin
* 4 -> Assistant Travel
* 3 -> Tournament Director
* 2 -> Webmaster
* 1 -> Social Chair(s)
* -1 -> Normie

Roles below 4 are currently unused.

`"img_name"` is a string that names an image in the
`mockchicago/static/img/member_photos` directory. All of the images
there need to have the same aspect ratio --- ideally the same
dimensions --- or it will look really bad. The dimensions of all of
the current images are 260x360px.

Once you have `mockchicago/data/members.json` correct and you have all
your images in `mockchicago/static/img/members_photos`, you're good to go.

### Making other edits (Optional)

The site is generated from a template, so you will need to edit the
template if you want to change other conent in the site.

Go into `mockchicago/templates` and find the file you want ---
probably `macro.html`. Make your changes. Things inside of `{{
brackets }}` get dynamically filled in by the templater and can
probably be left alone.

### Updating the database

Now run:

    python3 ./run.py -f mockchicago/data/members.json init

If all goes well, when you run

    python3 ./run.py run

You should see your changes on the site. If you do not, something has
gone wrong. Try running

    python3 ./run.py clean

And building the site again.

## Generating HTML

Run:

    python3 ./run.py freeze

You should now have a website waiting for you in the `mockchicago/build/` directory.

Aren't you glad that you didn't have to spend 45 minutes writing HTML
by hand to keep track of a bunch of useless news articles and awards
that no human being has ever looked at anyway? Yes. Yes you are.

## Publishing your changes

TODO

# Making Twitter work

TODO
