# Lightning Coindesk
A tutorial news app exemplifying Lightning Network micropayments integration.

Features a production-ready configuration for Heroku.

## Setup

Set up your virtual environment

```shell
mkdir ln-coindesk && cd ln-coindesk

virtualenv --python=/usr/bin/python2.7 deskenv
source deskenv/bin/activate

git clone https://github.com/MaxFangX/lightning-coindesk
cd lightning-coindesk

pip install -r requirements.txt
```

Run your local app!
```shell
python manage.py createsuperuser
python manage.py migrate
python manage.py runserver
```

View the Lightning Coindesk app at `localhost:8000`

## Deployment to Heroku

```shell
git init
git add -A
git commit -m "Initial commit"

heroku create
git push heroku master

heroku run python manage.py migrate
```

See also, a [ready-made application](https://github.com/heroku/python-getting-started), ready to deploy.

## License: MIT
