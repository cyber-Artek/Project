from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
import data



def get_db_connection():
     conn = sqlite3.connect('../database.db')
     conn.row_factory = sqlite3.Row
     return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts'). fetchall()
    conn.close()
    return render_template('index.html', posts = posts)


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)


    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']


        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                             ' WHERE id = ?',
                   (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))


    return render_template('edit.html', post=post)


@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))

@app.route('/house/')
def index1():
    return render_template('index1.html',
                           departures=data.departures,
                           title=data.title,
                           subtitle=data.subtitle,
                           description=data.description,
                           tours=data.tours)

@app.route('/departures/')
def departure_zero():
    return render_template('index1.html')

@app.route('/departures/<departure>/')
def departure(departure):
    tours = dict(filter(lambda tour: tour[1]["departure"] == departure, data.tours.items()))
    print(tours)
    if tours:
        return render_template('departure.html',
                               departure=departure,
                               title=data.title,
                               departures=data.departures,
                               tours=tours)
    abort(404)

@app.route('/tours/<int:id>/')
def tours(id):
    return render_template('tour.html',
                           tour=data.tours[id],
                           title=data.title,
                           departures=data.departures)

@app.route('/about')
def aboute():
    return render_template('aboute.html')



@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.username.data
    return render_template('registration.html', form=form)


if __name__=='__main__':
    app.run(debug=True)