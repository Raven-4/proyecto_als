from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SongForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    artist = StringField('Artista', validators=[DataRequired()])
    genre = StringField('Género', validators=[DataRequired()])
    submit = SubmitField('Guardar')
