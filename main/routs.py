import os

from flask import render_template, request, flash, url_for, redirect, g, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from main import app
from .db_worker import *


def allowed_file(filename):
    return '.' in filename and filename.split('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


def get_pair():
    current_gender = 'female' if g.user.u_gender == 'male' else 'male'
    persons = User.query.filter_by(u_gender=current_gender).all()
    current_person = None
    for person in persons:
        if not Match.query.all():
            current_person = person
            break
        if not Match.query.filter_by(mt_to_user=person.id, mt_from_user=g.user.id).first():
            current_person = person
            break
    if current_person:
        photo = Photo.query.filter_by(p_user=current_person.id).first()
        photo_src = photo.p_src
    else:
        photo_src = 'img/err_photo/no_avatar.png'
    return current_person, photo_src


def get_message(id_current_user: int):
    all_message_from_user = Message.query.filter_by(m_to_user=id_current_user, m_from_user=g.user.id).all()
    all_message_to_user = Message.query.filter_by(m_to_user=g.user.id, m_from_user=id_current_user).all()
    all_message = all_message_to_user + all_message_from_user
    all_message = sorted(all_message, key=lambda k: k.message_id)
    return all_message


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
def index():
    return render_template('index.html', title_name="Знакомства.ru")


@app.route('/home')
@login_required
def home():
    current_person, photo_src = get_pair()
    return render_template('home.html', title_name="Home", person=current_person, photo=photo_src)


@app.route('/login', methods=['POST'])
def login():
    phone = request.form.get('phone')
    password = request.form.get('password')
    if not (phone or password):
        flash('Заполните все поля')
        return render_template('index.html', title_name="Знакомства.ru")
    user = User.query.filter_by(u_phone=phone).first()
    if user and check_password_hash(user.u_password, password):
        login_user(user)
        return redirect('/home')
    flash('Номер или пароль введены неправильно')
    return render_template('index.html', title_name="Знакомства.ru")


@app.route('/info', methods=['POST'])
def registration():
    phone = request.form.get('phone')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')
    if request.method == 'POST':
        if not (phone or password or password_repeat):
            flash('Заполните все поля')
        elif password != password_repeat:
            flash('Пароли не совпадают')
        elif User.query.filter_by(u_phone=phone).first():
            flash('Пользователь с таким номером уже существует')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(u_phone=phone, u_password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return render_template('set_info.html')
    return redirect('/')


@app.route('/add_info', methods=['POST'])
@login_required
def add_info():
    name = request.form.get('name')
    surname = request.form.get('surname')
    age = request.form.get('age')
    gender = request.form.get('gender')
    city = request.form.get('city')
    about = request.form.get('about')
    file = request.files['file']

    if not (name or surname or age or gender or city or about or file or allowed_file(file)):
        flash("Заполните все поля")
    else:
        user = User.query.filter_by(u_phone=g.user.u_phone).first()
        user_src = f"main/static/img/{user.id}u/"
        os.mkdir(user_src)
        user.u_name = name
        user.u_surname = surname
        user.u_age = age
        user.u_city = city
        user.u_gender = gender
        user.u_src = user_src
        user.u_about = about
        filename = secure_filename(file.filename)
        path = os.path.join(user_src, filename)
        file.save(path)
        new_photo = Photo(p_src=path[11:], p_user=user.id)
        db.session.add(new_photo)
        db.session.commit()
        return redirect('/home')
    return render_template('/set_info')


@app.route('/cabinet')
@login_required
def cabinet():
    user = User.query.filter_by(u_phone=g.user.u_phone).first()
    photo = Photo.query.filter_by(p_user=user.id).first()
    return render_template('cabinet.html', title_name="Личный кабинет", user=user, photo=photo.p_src)


@app.route('/update_name', methods=['POST'])
@login_required
def update_name():
    new = request.form.get('name')
    if not new:
        flash('Введите имя')
    else:
        user = User.query.filter_by(u_phone=g.user.u_phone).first()
        user.u_name = new
        db.session.commit()
    return redirect('/cabinet')


@app.route('/update_surname', methods=['POST'])
@login_required
def update_surname():
    new = request.form.get('surname')
    if not new:
        flash('Введите фамилию')
    else:
        user = User.query.filter_by(u_phone=g.user.u_phone).first()
        user.u_surname = new
        db.session.commit()
    return redirect('/cabinet')


@app.route('/update_age', methods=['POST'])
@login_required
def update_age():
    new = request.form.get('age')
    if not new:
        flash('Введите возраст')
    else:
        user = User.query.filter_by(u_phone=g.user.u_phone).first()
        user.u_age = new
        db.session.commit()
    return redirect('/cabinet')


@app.route('/update_city', methods=['POST'])
@login_required
def update_city():
    new = request.form.get('city')
    if not new:
        flash('Введите город')
    else:
        user = User.query.filter_by(u_phone=g.user.u_phone).first()
        user.u_city = new
        db.session.commit()
    return redirect('/cabinet')


@app.route('/update_gender', methods=['POST'])
@login_required
def update_gender():
    new = request.form.get('gender')
    if not new:
        flash('Введите пол')
    else:
        user = User.query.filter_by(u_phone=g.user.u_phone).first()
        user.u_gender = new
        db.session.commit()
    return redirect('/cabinet')


@app.route('/match', methods=['POST'])
@login_required
def match():
    value = request.form.get('value')
    print(value)
    person_id = request.form.get('id')
    if value == "dislike":
        is_match = Match(mt_status=3, mt_to_user=person_id, mt_from_user=g.user.id)
        db.session.add(is_match)
        db.session.commit()
    elif value == "like":
        is_match = Match(mt_status=1, mt_to_user=person_id, mt_from_user=g.user.id)
        db.session.add(is_match)
        db.session.commit()
    elif value == "skip":
        is_match = Match(mt_status=2, mt_to_user=person_id, mt_from_user=g.user.id)
        db.session.add(is_match)
        db.session.commit()
    current_person, photo_src = get_pair()
    json_string = {"name": current_person.u_name, "surname": current_person.u_surname, "id": current_person.id,
                   "about": current_person.u_about, "img": photo_src, "age": current_person.u_age}
    return jsonify(json_string)


@app.route('/message', methods=['POST', 'GET'])
@login_required
def message():
    if request.method == "POST":
        person_id = request.form.get('write_message')
        person = User.query.filter_by(id=person_id).first()
        return redirect('/communication?id=' + str(person.id))
    match_start = Match.query.filter_by(mt_to_user=g.user.id).all()
    users = []
    photos = {}
    for match_in in match_start:
        user = User.query.filter_by(id=match_in.mt_from_user).first()
        users.append(user)
        photo = Photo.query.filter_by(p_user=user.id).first()
        photos |= {user.id: photo.p_src}
    return render_template('message.html', title_name="Message", users=users, photos=photos)


@app.route('/communication', methods=['GET'])
@login_required
def communication():
    user_id = request.args.get('id')
    user = User.query.filter_by(id=user_id).first()
    all_message = get_message(user.id)
    print(all_message)
    return render_template('communication.html', title_name="Сообщения", user=user, all_message=all_message)


@app.route('/send_msg', methods=['POST'])
@login_required
def send_msg():
    text = request.form.get('text')
    id_person = request.form.get('id')
    enter_time = request.form.get('time')
    print(text, id_person, enter_time)
    new_message = Message(m_datetime=enter_time, m_to_user=id_person, m_from_user=g.user.id, m_text=text)
    db.session.add(new_message)
    db.session.commit()
    json_sting = {"name": g.user.u_name, "text": text, "time": enter_time}
    return jsonify(json_sting)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')
