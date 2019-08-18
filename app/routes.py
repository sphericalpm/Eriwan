from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from werkzeug.datastructures import CombinedMultiDict


from app.forms import RegistrationForm, UploadJokeForm, LoginForm, EditJokeForm, EditUserProfileForm, EpisodeUploadForm
from app.models import User, Joke, Episode
from app import app, db
from app.utils import admin_required


@app.route('/')
def index():
    feed_blank = 'Podcast Main page: RSS feed'
    form = EpisodeUploadForm()
    return render_template('index.html', feed_blank=feed_blank, form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт успешно создан. Теперь Вы можете войти:', category='info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Неверное имя пользователя или пароль")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/'
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_joke', methods=['GET', 'POST'])
@admin_required
def add_joke_template():
    form = UploadJokeForm()
    if form.validate_on_submit():
        new_joke = Joke(joke_text=form.text.data,
                        user_id=current_user.id)
        db.session.add(new_joke)
        db.session.commit()
        flash('Шутка добавлена!')
    return render_template('add_joke.html', form=form)


<<<<<<< HEAD
@app.route('/upload-podcast', methods=['POST'])
def upload_podcast_handle():
    if not current_user.is_authenticated:
        return app.config['UNREGISTER_USER'], 500
    form = EpisodeUploadForm(CombinedMultiDict((request.files, request.form)))
    if form.validate():
        episode = Episode(
            name=form.title.data,
            user_id=current_user.get_id()
        )
        upload_folder = app.config['UPLOAD_PODCAST_FOLDER']
        static_path = app.config['MEDIA_ROOT']
        db.session.add(episode)
        db.session.flush()
        form.file.data.save(f'{static_path}{upload_folder}/{episode.id}.mp3')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('index.html', form=form, feed_blank='Podcast Main page: RSS feed')
=======
@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    episodes = Episode.query.filter_by(user_id=user.id)
    jokes = Joke.query
    return render_template('profile.html', user=user, joks=jokes, episodes=episodes)


@app.route('/jokes/edit_joke/<joke_id>', methods=['GET', 'POST'])
def edit_joke(joke_id):
    form = EditJokeForm()
    joke = Joke.query.filter_by(id=joke_id).first_or_404()
    if form.validate_on_submit():
        joke.joke_text = form.text.data
        db.session.add(joke)
        db.session.commit()
        flash('Ваши изменения сохранены!')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.text.data = joke.joke_text
    return render_template('edit_joke.html', form=form)


@app.route('/jokes/delete_joke/<joke_id>', methods=['GET', 'POST'])
def delete_joke(joke_id):
    joke = Joke.query.filter_by(id=joke_id).first_or_404()
    db.session.delete(joke)
    db.session.commit()
    flash("Успешно удалено")
    return redirect(url_for('profile', username=current_user.username))


@app.route('/user/edit_profile/<username>', methods=['GET', 'POST'])
def edit_profile(username):
    form = EditUserProfileForm()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        if current_user.id == user.id:
            if user.check_password(form.old_password.data):
                user.username = form.username.data
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Ваши изменения сохранены!')
                return redirect(url_for('profile', username=user.username))
            else:
                flash("Старый пароль неверный")
                return redirect(url_for("/user/edit_profile/", username=user.username))
        else:
            flash('Доступ запрещён')
    elif request.method == "GET":
        form.username.data = user.username
    return render_template('edit_joke.html', form=form)

