import re
from http import HTTPStatus
from urllib.parse import urljoin

from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_url(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': urlmap.original}), HTTPStatus.OK


@app.route('/api/id/', methods=('POST',))
def create_id():
    data = request.get_json()
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id') or get_unique_short_id()
    if not re.match(r'^[0-9a-zA-Z]{1,16}$', custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    urlmap = URLMap()
    urlmap.from_dict(dict(
        original=data['url'],
        short=custom_id,
    ))
    db.session.add(urlmap)
    db.session.commit()
    return jsonify(dict(
        url=urlmap.original,
        short_link=urljoin(request.url_root, urlmap.short),
    )), HTTPStatus.CREATED
