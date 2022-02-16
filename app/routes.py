from app import app
from flask import render_template, url_for, session, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegisterForm, AddPlaceOfCrime, DeletePlaceOfCrime, AddCrimeForm, ExecuteCrimeForm
from app.forms import UpdateCrimeOfVillainForm, UpdateAbilityOfHeroForm
from app.models import User, RoleOfUser, Superhero, Villain, SuperheroCrime, PlaceOfCrime, Crime
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
def index():
    if current_user.is_authenticated:
        print(current_user.get_id())
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()

    if login_form.submit.data:

        user = User.get_user_by_login(login_form.login.data)

        if user:

            if check_password_hash(user.password_of_user, login_form.password.data):

                login_user(user)
                session['role'] = user.id_of_role
                return redirect(url_for('index'))

            else:
                flash('Введён неверный пароль')
        else:
            flash('Пользователя с такими данными не существует')

    return render_template("login.html", login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():

    register_form = RegisterForm()
    list_of_all_roles = RoleOfUser.get_list_of_all_roles()
    register_form.select_role.choices = [i.name_of_role for i in list_of_all_roles]

    if register_form.submit.data:

        role = RoleOfUser.get_id_of_role_by_name_of_role(register_form.select_role.data)
        _hashed_password = generate_password_hash(register_form.password.data)

        User.add_user(register_form.login.data, _hashed_password, register_form.fio.data,
                      register_form.biography.data, role.id_of_role)
        id_user = User.get_id_of_user_by_login(register_form.login.data)

        if role.id_of_role == 1:
            Superhero.add_superhero(id_user.id_of_user)
        elif role.id_of_role == 2:
            Villain.add_villain(id_user.id_of_user)

        return redirect(url_for('login'))

    return render_template("register.html", register_form=register_form)


@app.route('/admin')
@login_required
def admin():
    if session['role'] == 3:
        return render_template("admin.html")
    elif session['role'] != 3:
        return redirect(url_for('index'))


@app.route('/place_of_crime', methods=['GET', 'POST'])
@login_required
def place_of_crime():
    if session['role'] == 3:

        places = PlaceOfCrime.get_all_places()

        add_place_of_crime = AddPlaceOfCrime()
        delete_place_of_crime = DeletePlaceOfCrime()

        if add_place_of_crime.submit_add.data:

            PlaceOfCrime.add_place_of_crime(add_place_of_crime.place.data)
            return redirect(url_for('place_of_crime'))

        if delete_place_of_crime.submit_delete.data:

            PlaceOfCrime.delete_place(delete_place_of_crime.id_of_place.data)
            return redirect(url_for('place_of_crime'))

        return render_template("place_of_crime.html", add_place_of_crime=add_place_of_crime,
                               delete_place_of_crime=delete_place_of_crime, places=places)
    elif session['role'] != 3:
        return redirect(url_for('index'))


@app.route('/crimes', methods=['GET', 'POST'])
def crimes():

    if session['role'] == 1:

        execute_crime_form = ExecuteCrimeForm()
        all_crimes = Crime.get_crimes_wo_current_hero(current_user.get_id())

        if execute_crime_form.submit_execute.data:

            SuperheroCrime.execute_crime(execute_crime_form.id_of_crime.data, current_user.get_id())

        return render_template("crimes.html", crimes=all_crimes, execute_crime_form=execute_crime_form)

    if session['role'] == 2:

        all_crimes = Crime.get_crimes_wo_current_villain(current_user.get_id())

        add_crime_form = AddCrimeForm()
        places = PlaceOfCrime.get_all_places()
        add_crime_form.place.choices = [i.name_of_place_of_crime for i in places]

        if add_crime_form.submit_add.data:

            id_of_place = PlaceOfCrime.get_id_of_place_by_name(add_crime_form.place.data)

            Crime.add_crime(add_crime_form.text.data, add_crime_form.date.data, id_of_place.id_of_place_of_crime,
                            add_crime_form.time.data)
            return redirect(url_for('crimes'))

        return render_template("crimes.html", add_crime_form=add_crime_form, crimes=all_crimes)


@app.route('/profile', methods=['GET', 'POST'])
def profile():

    if session['role'] == 1:

        crimes_for_hero = Crime.get_crimes_for_superhero(current_user.get_id())

        update_ability_of_hero_form = UpdateAbilityOfHeroForm()

        user = User.get_info_about_current_hero(current_user.get_id())

        if update_ability_of_hero_form.submit_update.data:

            Superhero.update_ability_of_hero(current_user.get_id(),
                                             update_ability_of_hero_form.text_of_ability.data)
            return redirect(url_for('profile'))

        return render_template("profile.html", user=user, update_ability_of_hero_form=update_ability_of_hero_form,
                               crimes=crimes_for_hero)

    if session['role'] == 2:

        update_crime_of_villain_form = UpdateCrimeOfVillainForm()

        user = User.get_info_about_current_villain(current_user.get_id())

        crimes_for_villain = Crime.get_crimes_for_villain(current_user.get_id())

        if update_crime_of_villain_form.submit_update.data:

            Villain.update_favourite_crime_villain(current_user.get_id(),
                                                   update_crime_of_villain_form.text_of_crime.data)
            return redirect(url_for('profile'))

        return render_template("profile.html", user=user, update_crime_of_villain_form=update_crime_of_villain_form,
                               crimes=crimes_for_villain)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))
