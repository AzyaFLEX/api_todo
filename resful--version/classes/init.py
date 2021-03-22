from flask_restful import abort, Resource
from data.__all_models import *
from data import db_session
import flask


def abort_(news_id, _class):
    session = db_session.create_session()
    data = session.query(_class).get(news_id)
    if not data:
        abort(404, message=f"data {data} not found")