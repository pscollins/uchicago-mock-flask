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

# Dealing with the webiste

All of the following should happen on your local machine.

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

Push over SFTP. I forget exactly how this works. You should edit this file to explain how to do it.

If I remember correctly, most FTP clients won't let you recursively upload a whole folder. I used `lftp`, and did something like:

	cd mockchicago/build
	lftp sftp://pscollins@webservices.uchicago.edu
	mirror -R

See
[this link](http://unix.stackexchange.com/questions/26934/using-sftp-to-transfer-a-directory), which is what I followed. YMMV on other OSes.


# Making Twitter work

All of the following should happen on an AWS instance.

The reason we need to go through all this trouble is that we need to make a request to Twitter to grab the recent tweets. We would like to do this with some really simple server-side code on our webserver, but UChicago doesn't let us run any server-side code.

That leaves us with two options:

1. Make the request in JS, on the client side, or
2. Set up this AWS instance.

The first option requires us to put our public and private Twitter keys into the HTML that we serve. We could do this --- and there's a good chance that no one would ever notice --- but then we would be terrible people. So we'll go with the second.

## Set up the remote instance

SSH in, clone this repo. Get openssl, with:

	sudo apt-get install openssl

(Assuming you've got an Ubuntu instance set up, which is what you should do in order to make this easier).

Now you need to get the public and private key for Twitter set up, which are kept out of version control because it would be just as bad to put them in to version control as it would be to serve them with HTML.

So:

	cd twitterhook
	make decrypt_conf

Now you'll be promted for a password --- which is the same as the password to the UChicago mock trial Twitter account. After you enter it, you'll have a file called `config.py` under twitterhook.

I stole this strategy from [here](http://ejohn.org/blog/keeping-passwords-in-source-control/).

## Fix up your new URL

It would be nice if you registered a domain name for your AWS instance, but you don't need to. You can use a service like NameCheap, which will give you a free domain.

Now edit `uchicago-mock-flask/mockchicago/views.py` and change `REMOTE_URL` to:

	REMOTE_URL = //YOUR_AWS_INSTANCE_GOES_HERE

Where `YOUR_AWS_INSTANCE_GOES_HERE` is either the IP or URL that points to your AWS instance.

## Kick off the server

Run

	python3 ./run.py twitter

and it should just work. If it doesn't, talk to me.

# Outstanding issues

The size of images that come out of Twitter is awkward: we don't resize them, so they can be horribly misaligned. A better person than me could change it so that we grab a thumbnail (of a pre-known size) to keep the grid of images from Twitter a regular size.
