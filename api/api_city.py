import flask
from data.__all_models import User
from data import db_session

blueprint = flask.Blueprint(
    'city',
    __name__,
    template_folder='templates'
)


@blueprint.route('/users_show/<int:user_id>')
def show_city(user_id):
    db_sess = db_session.create_session()
    data = db_sess.query(User).get(user_id).to_dict()
    if not data or "city_from" not in data or data["city_from"] is None:
        return f'<h1>Bad request</h1>'
    return f'<h1>{data}</h1>'
