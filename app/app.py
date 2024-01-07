import os, requests
from flask import Flask, render_template
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    url = os.getenv("MEDIA_ENDPOINT")
    pw = os.getenv("MEDIA_ENDPOINT_PW")

    mr = requests.get(url + '?ls&pw=' + pw, timeout=1)

    media = mr.json()
    num_media = len(media['files'])
    num_rand = randint(0,num_media-1)

    rand_media_ext = media['files'][num_rand]['ext']

    if rand_media_ext in ['jpg','png','webp','gif']:
        rand_media_type = 'image'
    else:
        rand_media_type = 'video'

    rand_media_url = url + media['files'][num_rand]['href']

    return render_template('home.html', media_type=rand_media_type,media_url=rand_media_url)
