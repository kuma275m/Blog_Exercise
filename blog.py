from flask import *
from flask_login import (LoginManager, login_required, login_user, current_user, logout_user, UserMixin)
from wtforms import form, fields, validators, TextField, PasswordField
import db

app = Flask(__name__)
CSRF_ENABLED = True
app.secret_key = 'you-will-never-guess'

class User():
    username = 'admin'
    password = '123456'
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

def is_login():
    if 'is_authenticated' not in session:
	return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def index():
    entry = db.show_entry()
    return render_template('index.html', entry=entry)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
	keyword = request.form['key']
	result = db.search_post(keyword)
    return render_template('index.html', result=result)

@app.route('/viewpost/<id>')
def viewpost(id):
    post = db.view_post(id)
    return render_template('post.html', post=post)

@app.route('/add', methods=['GET', 'POST'])
def add():
    is_login()
    if request.method == 'POST':
	title = request.form['title']
	content = request.form['content']
	tags = request.form['tags']
	db.add_entry(title, content, tags)
	return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<id>')
def delete(id):
    is_login()
    db.delete_post(id)
    return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    is_login()
    post = db.view_post(id)
    if request.method == 'POST':
	title = request.form['title']
	content = request.form['content']
	tags = request.form['tags']
	db.edit_entry(id, title, content, tags)	
	return redirect(url_for('index'))
    return render_template('edit.html', post=post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	if request.form['username'] != User.username or request.form['password'] != User.password:
		error = 'Your username or password is not correct!'
	else:
		user = User.username
		session['is_authenticated'] = True
        	return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    is_login()
    session.pop('is_authenticated', None)
    return redirect (url_for('index'))

if __name__ == '__main__':
    app.debug = True
    app.run()
