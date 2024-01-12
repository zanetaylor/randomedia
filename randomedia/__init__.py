import os, requests
from dotenv import load_dotenv
from flask import Flask, render_template
from random import randint

load_dotenv('.env')

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def index():

        api_url = os.getenv("MEDIA_ENDPOINT_URL")
        api_category = os.getenv("MEDIA_DEFAULT_CATEGORY")

        category_request = api_request = requests.get(api_url + '?ls', timeout=1)
        categories = category_request.json()

        api_request = requests.get(api_url + api_category + '?ls', timeout=1)
        media = api_request.json()
        
        num_media = len(media['files'])
        num_rand = randint(0,num_media-1)

        rand_media_ext = media['files'][num_rand]['ext']

        if rand_media_ext in ['jpg','png','webp','gif']:
            rand_media_type = 'image'
        else:
            rand_media_type = 'video'

        rand_media_url = api_url + api_category + '/' + media['files'][num_rand]['href']

        return render_template('home.html', categories=categories['dirs'],media_type=rand_media_type,media_url=rand_media_url)
    
    @app.route('/<category>')
    def from_category(category):

        api_url = os.getenv("MEDIA_ENDPOINT_URL")

        api_request = requests.get(api_url + category + '?ls', timeout=1)
        media = api_request.json()

        num_media = len(media['files'])
        num_rand = randint(0,num_media-1)

        rand_media_ext = media['files'][num_rand]['ext']

        if rand_media_ext in ['jpg','png','webp','gif']:
            rand_media_type = 'image'
        else:
            rand_media_type = 'video'

        rand_media_url = api_url + category + '/' + media['files'][num_rand]['href']

        return render_template('home.html', media_type=rand_media_type,media_url=rand_media_url)

    return app
