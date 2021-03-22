from flask import Flask, make_response, jsonify
from data import db_session
from data.__all_models import User
from api import api_jobs, api_user, api_city

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': f'Not found: {error}'}), 404)


def main():
    db_session.global_init("db/users.db")
    app.register_blueprint(api_jobs.blueprint)
    app.register_blueprint(api_user.blueprint)
    app.register_blueprint(api_city.blueprint)
    app.run()


if __name__ == '__main__':
    main()
