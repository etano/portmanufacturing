Portmanufacturing
=================

Command central for [@portmanatee](https://twitter.com/portmanatee) using twitter bot model from [kicks-and-giggles](https://github.com/robincamille/kicks-and-giggles).

Get API info here: https://apps.twitter.com/app/5465048/keys

To get running:

    sudo pip install tweepy
    python portmanufacture.py

For crontab (every hour):

    0 * * * * /usr/bin/python /path/to/portmanufacturing/portmanufacture.py >> /path/to/portmanufacturing/portmanufacture.log 2>&1
