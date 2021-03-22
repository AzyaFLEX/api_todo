from .init import *


class UsersListResource(Resource):
    def post(self):
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

    def put(self, user_id):
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
