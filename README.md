# twitter-archiver
Save a user's tweets to the Wayback Machine.

#### Setup
 Install
 * [Docker](https://docs.docker.com/engine/install/)
 * [Docker Compose](https://docs.docker.com/compose/install/)

#### Use
 * Set the users whose tweets you want to archive in settings.py
 * Rebuild the image with `docker-compose build`
 * Run the archiver with `docker-compose run twitter-archiver`

#### Notes


Uses SQLite and Firefox + geckodriver by default but should work with other databases and browsers with relatively
minor tweaking.

I know Twitter has a search API but I don't want to beg them for a developer account or be bound by their developer
policy, much less force potential users to do the same.
