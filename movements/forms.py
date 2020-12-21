from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField, FloatField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length
from datetime import date


def must_be_before_today(form, field):
    today = date.today()
    if field.data > today:
        raise ValidationError('La fecha no puede ser posterior a hoy')


class MovementForm(FlaskForm):
    fecha = DateField('Fecha', validators=[DataRequired(), must_be_before_today])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=10, message="El concepto debe tener más de 10 caracteres")])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])

    submit = SubmitField('Aceptar')

