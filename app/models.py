from flask_login import UserMixin
from app import db
from app import login_manager
from flask import flash, redirect, url_for


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = '_user'
    __table_args__ = {'extend_existing': True}

    def get_id(self):
        return self.id_of_user

    @staticmethod
    def get_user_by_login(login):
        try:
            query = db.session.query(User).filter(User.login_of_user == login).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('login'))

    @staticmethod
    def add_user(login, password, fio, biography, role):
        user_to_add = User(login_of_user=login, password_of_user=password, fio_of_user=fio, id_of_role=role,
                           biography_of_user=biography)
        try:
            db.session.add(user_to_add)
            db.session.commit()
            flash('Пользователь успешно добавлен')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def get_id_of_user_by_login(login):
        try:
            query = db.session.query(User)
            query = query.filter(User.login_of_user == login)
            return query.one()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('login'))

    @staticmethod
    def get_info_about_current_hero(id_user):
        try:
            query = db.session.query(User, RoleOfUser, Superhero)
            query = query.join(RoleOfUser, User.id_of_role == RoleOfUser.id_of_role)
            query = query.join(Superhero, User.id_of_user == Superhero.id_of_superhero)
            query = query.filter(User.id_of_user == id_user)
            return query.one()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('profile'))

    @staticmethod
    def get_info_about_current_villain(id_user):
        try:
            query = db.session.query(User, RoleOfUser, Villain)
            query = query.join(RoleOfUser, User.id_of_role == RoleOfUser.id_of_role)
            query = query.join(Villain, User.id_of_user == Villain.id_of_villain)
            query = query.filter(User.id_of_user == id_user)
            return query.one()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('profile'))


class RoleOfUser(db.Model):
    __tablename__ = 'role_of_user'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_list_of_all_roles():
        try:
            query = db.session.query(RoleOfUser).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def get_id_of_role_by_name_of_role(name_role):
        try:
            query = db.session.query(RoleOfUser).filter(RoleOfUser.name_of_role == name_role).one()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))


class Superhero(db.Model):
    __tablename__ = 'superhero'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_superhero(id_user):
        hero_to_add = Superhero(id_of_superhero=id_user)
        try:
            db.session.add(hero_to_add)
            db.session.commit()
            flash('Супергерой успешно добавлен')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def update_ability_of_hero(id_user, ability):
        try:
            ability_to_update = db.session.query(Superhero).filter(Superhero.id_of_superhero == id_user).first()
            ability_to_update.ability_of_superhero = ability
            db.session.commit()
            flash('Способность героя успешно обновлена')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('profile'))


class Villain(db.Model):
    __tablename__ = 'villain'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_villain(id_user):
        villain_to_add = Villain(id_of_villain=id_user)
        try:
            db.session.add(villain_to_add)
            db.session.commit()
            flash('Злодей успешно добавлен')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('register'))

    @staticmethod
    def update_favourite_crime_villain(id_user, crime):
        try:
            villain_to_update = Villain.query.filter(Villain.id_of_villain == id_user).first()
            villain_to_update.favorite_crime_of_villain = crime
            db.session.commit()
            flash('Любимое злодейство успешно обновлено')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('profile'))


class PlaceOfCrime(db.Model):
    __tablename__ = 'place_of_crime'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def add_place_of_crime(name):
        place_to_add = PlaceOfCrime(name_of_place_of_crime=name)
        try:
            db.session.add(place_to_add)
            db.session.commit()
            flash('Место преступления успешно добавлено')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('add_place'))

    @staticmethod
    def get_id_of_place_by_name(name):
        try:
            query = db.session.query(PlaceOfCrime)
            query = query.filter(PlaceOfCrime.name_of_place_of_crime == name)
            return query.one()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('crime'))

    @staticmethod
    def get_all_places():
        try:
            query = db.session.query(PlaceOfCrime).all()
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('add_place'))

    @staticmethod
    def delete_place(_id):
        try:
            db.session.query(PlaceOfCrime).filter(PlaceOfCrime.id_of_place_of_crime == _id).delete()
            db.session.commit()
            flash('Место преступления успешно удалено')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('add_place'))


class Crime(db.Model):
    __tablename__ = 'crime'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def get_all_crimes():
        try:
            query = db.session.query(Crime, PlaceOfCrime)
            query = query.join(PlaceOfCrime, Crime.id_of_place_of_crime == PlaceOfCrime.id_of_place_of_crime)
            return query
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('crime'))

    @staticmethod
    def add_crime(text, date, place, time):
        crime_to_add = Crime(id_of_place_of_crime=place, date_of_crime=date, text_of_crime=text, time_of_crime=time)
        try:
            db.session.add(crime_to_add)
            db.session.commit()
            flash('Преступление успешно добавлено')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('crimes'))

    @staticmethod
    def get_crimes_wo_current_villain(id_villain):
        try:
            query = db.session.query(Crime, PlaceOfCrime)
            query = query.join(PlaceOfCrime, Crime.id_of_place_of_crime == PlaceOfCrime.id_of_place_of_crime)
            query = query.filter(Crime.id_of_villain != id_villain)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('crimes'))

    @staticmethod
    def get_crimes_wo_current_hero(id_hero):
        try:
            query = db.session.query(Crime, PlaceOfCrime)
            query = query.join(PlaceOfCrime, Crime.id_of_place_of_crime == PlaceOfCrime.id_of_place_of_crime)
            query = query.join(SuperheroCrime, SuperheroCrime.id_of_crime == Crime.id_of_crime)
            query = query.filter(SuperheroCrime.id_of_superhero != id_hero)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('crimes'))

    @staticmethod
    def get_crimes_for_villain(id_villain):
        try:
            query = db.session.query(Crime, PlaceOfCrime)
            query = query.join(PlaceOfCrime, Crime.id_of_place_of_crime == PlaceOfCrime.id_of_place_of_crime)
            query = query.filter(Crime.id_of_villain == id_villain)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('profile'))

    @staticmethod
    def get_crimes_for_superhero(id_hero):
        try:
            query = db.session.query(Crime, PlaceOfCrime, SuperheroCrime)
            query = query.join(SuperheroCrime, Crime.id_of_crime == SuperheroCrime.id_of_crime)
            query = query.join(PlaceOfCrime, Crime.id_of_place_of_crime == PlaceOfCrime.id_of_place_of_crime)
            query = query.filter(SuperheroCrime.id_of_superhero == id_hero)
            return query.all()
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('profile'))


class SuperheroCrime(db.Model):
    __tablename__ = 'superhero_crime'
    __table_args__ = {'extend_existing': True}

    @staticmethod
    def execute_crime(id_crime, id_superhero):
        crime_to_execute = SuperheroCrime(id_of_superhero=id_superhero, id_of_crime=id_crime)
        try:
            db.session.add(crime_to_execute)
            db.session.commit()
            flash('Злодеи не дремлют! Супергерои тоже:)')
        except:
            flash('Ошибка взаимодействия с базой данных! Попробуйте позже!')
            return redirect(url_for('crimes'))
