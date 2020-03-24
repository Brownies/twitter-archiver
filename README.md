# twitter-archiver
Save a user's tweets to the Wayback Machine.

#### Setup
 * Install
 [Firefox](https://www.mozilla.org/en-US/firefox/new/),
 [geckodriver](https://github.com/mozilla/geckodriver/releases)
 and [SQLite](https://sqlite.org/download.html)
 * `git clone git@github.com:Brownies/twitter-archiver.git`
 * `cd twitter-archiver`
 * `pip install -r requirements.txt`(Use `pip3` on Linux/Mac)
 

#### Use
 * Set the users whose tweets you want to archive in settings.py
 * `python twitter-archiver.py`(Use `python3` on Linux/Mac)

#### Notes


Uses SQLite and Firefox + geckodriver by default but should work with other databases and browsers with relatively
minor tweaking.

I know Twitter has a search API but I don't want to beg them for a developer account or be bound by their developer
policy, much less force potential users to do the same.
