import flask
from data.__all_models import User
from data import db_session

blueprint = flask.Blueprint(
    'user',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user', methods=['GET'])
def get_user():
    db_sess = db_session.create_session()
    data = db_sess.query(User).all()
    return flask.jsonify({'users': [elm.to_dict() for elm in data]})


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_id(user_id):
    db_sess = db_session.create_session()
    data = db_sess.query(User).get(user_id)
    if data:
        return flask.jsonify({'user': data.to_dict()})
    return flask.jsonify({'error': 'missed id'})


@blueprint.route('/api/user', methods=['POST'])
def create_user():
    try:
        if not flask.request.json:
            return flask.jsonify({'error': 'Empty request'})
        elif not all(key in flask.request.json for key in
                     list(filter(lambda x: "__" not in x and "_sa" not in x, list(vars(User))))):
            return flask.jsonify({'error': 'Bad request'})
        db_sess = db_session.create_session()
        user_id = db_sess.query(User).get(flask.request.json['id'])
        if user_id:
            return flask.jsonify({'error': 'Id already exists'})
        m_data = list(filter(lambda x: "__" not in x and "_sa" not in x, list(vars(User))))
        user = User()
        for elm in m_data:
            exec(f'user.{elm} = flask.request.json["{elm}"]')
        db_sess.add(user)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})
    except BaseException as error:
        with open("logs/api.txt", "w") as file:
            file.write(error)


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return flask.jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def redo_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    m_data = list(filter(lambda x: "__" not in x and "_sa" not in x, list(vars(User))))
    m_data.remove('id')
    if not user:
        return flask.jsonify({'error': 'Not found'})
    elif not all(key in flask.request.json for key in m_data):
        return flask.jsonify({'error': f'missed: {list(filter(lambda x: x not in flask.request.json, m_data))}'})
    for elm in m_data:
        exec(f'user.{elm} = flask.request.json["{elm}"]')
    db_sess.commit()
    return flask.jsonify({'success': 'OK'})

