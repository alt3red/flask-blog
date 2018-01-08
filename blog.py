from flask import Flask, render_template, request, session, flash, redirect, url_for, g
import sqlite3
from functools import wraps

# configuration
DATABASE = 'blog.db'
USERNAME = 'admin'
PASSWORD = 'admin'
SECRET_KEY = 'very_secret_key'

app = Flask(__name__)

app.config.from_object(__name__)


def connect_db():
    return


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to login first!")
            return redirect(url_for('login'))
    return wrap


sqlite3.connect(app.config['DATABASE'])


@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    status_code = 200
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid credentials, please try again!'
            status_code = 401
        else:
            session['logged_in'] = True
            return redirect(url_for('main'))
        return render_template('login.html', error=error), status_code
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You are logged out.")
    return redirect(url_for('login'))


@app.route('/main')
@login_required
def main():
    return render_template('main.html')


if __name__ == '__main__':
    app.run(debug=True)