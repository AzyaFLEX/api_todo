from .init import *


class UsersResource(Resource):
    def get(self, user_id):
        db_sess = db_session.create_session()
        data = db_sess.query(User).get(user_id)
        if data:
            return flask.jsonify({'user': data.to_dict()})
        return flask.jsonify({'error': 'missed id'})

    def delete(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        if not user:
            return flask.jsonify({'error': 'Not found'})
        db_sess.delete(user)
        db_sess.commit()
        return flask.jsonify({'success': 'OK'})
