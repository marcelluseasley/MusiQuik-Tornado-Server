from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy

# mysql://username:password@hostname/database
# add_search, add_download, searches, downloads, add_dmca_request
app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://musiquik:musiquik@localhost/musiquik'
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
