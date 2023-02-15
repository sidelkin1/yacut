from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional, Regexp


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(
            DataRequired(message='Обязательное поле'),
            URL(message='Введите адрес URL'),
            Length(max=256),
        )
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(
            Regexp(
                r'^[0-9a-zA-Z]{1,16}$',
                message='Указано недопустимое имя для короткой ссылки',
            ),
            Length(max=16),
            Optional(strip_whitespace=False),
        )
    )
    submit = SubmitField('Создать')
