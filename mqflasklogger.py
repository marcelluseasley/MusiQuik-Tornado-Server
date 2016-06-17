from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from urlparse import urlparse
import requests
from bs4 import BeautifulSoup
import json
from collections import defaultdict

# mysql://username:password@hostname/database
# add_search, add_download, searches, downloads, add_dmca_request

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://musiquik:musiquik@localhost/musiquik'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Search(db.Model):
    __tablename__ = 'searches'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.String(255), nullable=False)
    request_ip = db.Column(db.String(128), nullable=False)
    searched = db.Column(db.DateTime, nullable=False)

    def __init__(self, query, request_ip, searched):
        self.query = query
        self.request_ip = request_ip
        self.searched = searched

    def __repr__(self):
        return '<Search %r>' % self.query


class Download(db.Model):
    __tablename__ = 'downloads'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    query = db.Column(db.String(255), nullable=False)
    request_ip = db.Column(db.String(128), nullable=False)
    song = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    direct_url = db.Column(db.String(512), nullable=False)
    downloaded = db.Column(db.DateTime, nullable=False)

    def __init__(self, query, request_ip, song, artist, direct_url, downloaded):
        self.query = query
        self.request_ip = request_ip
        self.song = song
        self.artist = artist
        self.direct_url = direct_url
        self.downloaded = downloaded

    def __repr__(self):
        return '<Download %r>' % self.query


@app.route('/add_search', methods=['POST'])
def add_search():
    search = Search(request.form['query'], request.form['request_ip'], request.form['searched'])

    db.session.add(search)
    db.session.commit()

    return ('', 204)


@app.route('/add_download', methods=['POST'])
def add_download():
    download = Download(request.form['query'], request.form['request_ip'], request.form['song'], request.form['artist'],
                        request.form['direct_url'], request.form['downloaded'])

    db.session.add(download)
    db.session.commit()

    return ('', 204)


@app.route('/searches', methods=['GET'])
def searches():
    return "lala"


@app.route('/downloads', methods=['GET'])
def downloads():
    pass

@app.route('/getsongs', methods=['POST'])
def getsong():

    searchTerm = request.form['query']
    url = "http://mp3monkey.net/searchProxy.php"

    tracklist = defaultdict()
    tracklist['tracks'] = list()

    headers = {"Host": getDomainName(url),
               "Origin": getDomainName(url),
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
               "Content-Type": "application/x-www-form-urlencoded",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Language": "en-US,en;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Upgrade-Insecure-Requests": "1",
               "Cache-Control": "no-cache",
               "Pragma": "no-cache",
               "Referer": getDomainName(url),
               "Connection": "keep-alive"}

    payload = {'search': searchTerm}

    resp = requests.post(url, payload, allow_redirects=True, timeout=5000.0, headers=headers)
    resp.encoding = 'utf-8'

    #print("status_code: {}".format(resp.status_code))
    #print(resp.text)

    soup = BeautifulSoup(resp.text, 'html.parser')

    resultset = soup.find_all("div", class_="results")
    songset = resultset[0].find_all("div", class_="toggle")

    for songNode in songset:
        (artist, song) = songNode.b.text.split("-", 1)

        artist = artist.replace('"', '', 10)
        song = song.replace('"', '', 10)
        print(artist)
        print(song)

        preUrl = songNode.find_all("div", class_="floatRight")[0].find_all("a", {"rel": "nofollow"})[0]["href"]

        headers2 = {"Host": getDomainName(preUrl),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate, sdch",
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"}

        resp2 = requests.get(preUrl, allow_redirects=True, timeout=10000.0)
        resp2.encoding = 'utf-8'

        soup2 = BeautifulSoup(resp2.text, 'html.parser')

        directUrl = soup2.find_all(id="content")[0].find_all("a", class_="green")[0]["href"]
        print(directUrl)
        print()

        tracklist["tracks"].append({"name": song, "artist": artist, "direct": directUrl})
    tracklist = json.dumps(tracklist)
    print(tracklist)


# helper functions
def getDomainName(url):
    dName = urlparse(url).netloc
    if dName.startswith('www.'):
        dName = dName[4:]
    return dName

