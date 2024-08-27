from flask import Flask, request, redirect, render_template_string
import sqlite3
import hashlib
import os
import validators

app = Flask(__name__)

# Database setup
DATABASE = 'urls.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as db:
        db.execute('''CREATE TABLE IF NOT EXISTS urls
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, short TEXT, long TEXT)''')

@app.before_first_request
def setup():
    if not os.path.exists(DATABASE):
        init_db()

@app.route('/')
def home():
    return render_template_string('''
        <form action="/shorten" method="post">
            <input type="text" name="url" placeholder="Enter URL to shorten" required>
            <button type="submit">Shorten</button>
        </form>
    ''')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']

    # Validate URL
    if not validators.url(long_url):
        return 'Invalid URL', 400

    short_id = hashlib.md5(long_url.encode()).hexdigest()[:6]

    with get_db() as db:
        # Check if URL is already shortened
        existing_entry = db.execute('SELECT short FROM urls WHERE long = ?', (long_url,)).fetchone()
        if existing_entry:
            return f'URL already shortened: <a href="/{existing_entry["short"]}">/{existing_entry["short"]}</a>'

        db.execute('INSERT INTO urls (short, long) VALUES (?, ?)', (short_id, long_url))
        db.commit()

    return f'Shortened URL: <a href="/{short_id}">/{short_id}</a>'

@app.route('/<short_id>')
def redirect_to_long_url(short_id):
    with get_db() as db:
        url = db.execute('SELECT long FROM urls WHERE short = ?', (short_id,)).fetchone()
        if url:
            return redirect(url['long'])
        else:
            return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)
