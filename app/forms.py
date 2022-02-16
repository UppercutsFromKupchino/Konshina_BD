from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField, TimeField, DateField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Авторизуйтесь")


class RegisterForm(FlaskForm):
    login = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    fio = StringField()
    biography = StringField()
    select_role = SelectField(choices=[])
    submit = SubmitField("Зарегистрируйтесь")


class AddPlaceOfCrime(FlaskForm):
    place = StringField(validators=[DataRequired()])
    submit_add = SubmitField("Добавьте место преступления")


class DeletePlaceOfCrime(FlaskForm):
    id_of_place = HiddenField()
    submit_delete = SubmitField("Удалить место преступления")


class AddCrimeForm(FlaskForm):
    text = StringField(validators=[DataRequired()])
    place = SelectField(choices=[])
    date = DateField()
    time = TimeField()
    submit_add = SubmitField("Добавить преступление")


class ExecuteCrimeForm(FlaskForm):
    id_of_crime = HiddenField()
    submit_execute = SubmitField("Остановите злодея!")


class UpdateCrimeOfVillainForm(FlaskForm):
    text_of_crime = StringField(validators=[DataRequired()])
    submit_update = SubmitField("Обновить данные")


class UpdateAbilityOfHeroForm(FlaskForm):
    text_of_ability = StringField(validators=[DataRequired()])
    submit_update = SubmitField("Обновить данные")
