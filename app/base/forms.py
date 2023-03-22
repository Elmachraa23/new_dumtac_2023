# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired, EqualTo
from .models import User
from wtforms import ValidationError, validators
from app.base.tools import verify_pass

# login and registration


class SigninForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    def __init__(self, *k, **kk):
        self._user = None  # for internal user storing
        super(SigninForm, self).__init__(*k, **kk)

    def validate(self):
        self._user = User.query.filter_by(email=self.email.data).first()
        return super(SigninForm, self).validate()

    def validate_email(self, field):
        if self._user is None:
            raise ValidationError("Ce compte n'existe pas. Veuillez vérifier votre e-mail !")
        if not self._user.is_active:
            raise ValidationError("Votre compte n'est pas encore activé. Veuillez contacter l'administrateur!")

    def validate_password(self, field):
        if self._user is None:
            raise ValidationError()  # just to be sure
        if not verify_pass(field.data, self._user.password):  # passcheck embedded into user model
            raise ValidationError("Mot de passe incorrect. Veuillez vérifier votre mot de passe !")
