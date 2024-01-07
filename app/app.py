import os, requests
from flask import Flask, render_template
from random import randint

app = Flask(__name__)

@app.route('/')
def index():
    url = os.getenv("MEDIA_ENDPOINT")
    pw = os.getenv("MEDIA_ENDPOINT_pw")

    mr = requests.get(url + '?ls&pw=' + pw, timeout=1)

    memes = mr.json()
    num_memes = len(memes['files'])
    num_rand = randint(0,num_memes-1)

    rand_meme_ext = memes['files'][num_rand]['ext']

    if rand_meme_ext in ['jpg','png','webp','gif']:
        rand_meme_type = 'image'
    else:
        rand_meme_type = 'video'

    rand_meme_url = url + memes['files'][num_rand]['href']

    return render_template('home.html', meme_type=rand_meme_type,meme_url=rand_meme_url)
