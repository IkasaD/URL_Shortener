from flask import Flask, request, redirect, render_template, url_for
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'

engine = create_engine('sqlite:///urls.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class URL(Base):
    __tablename__ = 'urls'
    id = Column(Integer, primary_key=True)
    long_url = Column(String)
    short_url = Column(String)

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['nm']
    session = Session()

    existing_url = session.query(URL).filter_by(long_url=long_url).first()
    if existing_url:
        return render_template('short_url.html',short_url = existing_url.short_url)

    short_url = generate_short_url()
    url = URL(long_url=long_url, short_url=short_url)
    session.add(url)
    session.commit()
    return render_template('short_url.html',short_url= short_url)

def generate_short_url():
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(6))
    return short_url

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    session = Session()
    url = session.query(URL).filter_by(short_url=short_url).first()
    return redirect(url.long_url) if url else 'URL not found'

@app.route('/database')
def database():
    session = Session()
    data = session.query(URL).all()
    return render_template('database.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
