import random
import string

from flask import flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id(length=6):
    while True:
        short = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=length,
            )
        )
        if URLMap.query.filter_by(short=short).first() is None:
            break
    return short


@app.route('/', methods=('GET', 'POST'))
def index_view():
    form = URLMapForm()
    urlmap = None
    if form.validate_on_submit():
        short = form.custom_id.data or get_unique_short_id()
        if URLMap.query.filter_by(short=short).first() is not None:
            flash(f'Имя {short} уже занято!')
            return render_template('index.html', form=form)
        original = form.original_link.data
        urlmap = URLMap.query.filter_by(original=original).first()
        if urlmap is None:
            urlmap = URLMap(
                original=original,
                short=short,
            )
            db.session.add(urlmap)
            db.session.commit()
        else:
            flash('Такая ссылка уже есть в базе!')
    return render_template('index.html', form=form, urlmap=urlmap)


@app.route('/<short>')
def original_view(short):
    urlmap = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(urlmap.original)
